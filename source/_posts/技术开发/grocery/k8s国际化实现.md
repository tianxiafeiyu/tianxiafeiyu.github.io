k8s用的是 github.com/gosexy/gettext/go-xgettext 翻译库

项目中提供shell脚本，通过翻译库自带的 go-xgettext 工具进行词条扫描，生成template.po文件

不支持增量扫描