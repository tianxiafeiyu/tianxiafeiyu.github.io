#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
文章格式转换工具，为md文档添加
```
title: xxx
```
样式
1. python tools.py format_hexo source/_posts/
    目录下所有md文件统计添加head
2. python tools.py unformat_hexo source/_posts/
    目录下所有md文件删除head
"""
import datetime
import os
import sys

MUST_HEADS = ['title', 'date', 'updated', 'toc', 'tags']


def _remove_file_head(filename):
    head_map = dict()
    nums = 0
    lines = None
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if lines and lines[0].rstrip() != '---':
            return head_map, lines

        lines = lines[1:len(lines)]
        for line in lines:
            lines = lines[1:len(lines)]
            line = line.rstrip()
            if line.rstrip() == '---':
                break
            head_kv = line.split(': ')
            if len(head_kv) == 2:
                head_map[head_kv[0]] = head_kv[1]
            # 如果表头元数据太多了，显然不正常，放弃修改
            if nums > 10:
                head_map = dict()
                return head_map, lines

    return head_map, lines


def format_hexo(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if not file.endswith('.md'):
                continue
            full_name = os.path.join(root, file)
            old_head_map, old_lines = _remove_file_head(full_name)

            if len(old_head_map) >= len(MUST_HEADS):
                continue

            head_lines = ['---\n']
            tpl_str = '{}: {}\n'
            filename = file.split('.md')[0]
            for head in MUST_HEADS:
                if old_head_map.get(head):
                    head_lines.append(tpl_str.format(head, old_head_map.get(head)))
                    continue
                if head == 'title':
                    head_lines.append(tpl_str.format(head, filename))
                elif head == 'date':
                    ctime = int(os.path.getctime(full_name))
                    head_lines.append(tpl_str.format(head, datetime.datetime.fromtimestamp(ctime)))
                elif head == 'updated':
                    mtime = int(os.path.getmtime(full_name))
                    head_lines.append(tpl_str.format(head, datetime.datetime.fromtimestamp(mtime)))
                elif head == 'toc':
                    head_lines.append(tpl_str.format(head, 'true'))
                elif head == 'tags':
                    line = '{}: \n    - {}\n'.format(head, filename)
                    head_lines.append(line)
            head_lines.append('---\n')

            with open(full_name, 'w', encoding='utf-8') as f:
                for line in head_lines:
                    f.write(line)
                for line in old_lines:
                    f.write(line)

        for dir in dirs:
            format_hexo(os.path.join(root, dir))


def unformat_hexo(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if not file.endswith('.md'):
                continue
            full_name = os.path.join(root, file)
            old_head_map, old_lines = _remove_file_head(full_name)

            with open(full_name, 'w', encoding='utf-8') as f:
                for line in old_lines:
                    f.write(line)

        for dir in dirs:
            unformat_hexo(os.path.join(root, dir))


def main():
    func_name = sys.argv[1]
    file_dir = sys.argv[2]
    if not os.path.exists(file_dir):
        print('file path not exist: %s' % file_dir)
        return
    func = getattr(sys.modules[__name__], func_name)

    func(file_dir)


if __name__ == '__main__':
    main()
