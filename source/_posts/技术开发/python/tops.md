所谓 tips 记录，就是在实际工作学习中需要上网查找资料，得到满意答案后的记录，避免经常重复查询。

记录原则，精简有效，只记录满意的答案，尽量不要发散

#### 1. os.path.basename、 os.path.dirname

获取路径的文件名，文件夹

    os.path.basename("/tmp/test/test.txt")
    # test.txt

    os.path.dirname("/tmp/test/test.txt")
    # /tmp/test

### sqlalchemy更新
```
1) for c in session.query(Stuff).all():
       c.foo += 1
   session.commit()

2) session.query().\
       update({"foo": (Stuff.foo + 1)})
   session.commit()

3) conn = engine.connect()
   stmt = Stuff.update().\
       values(Stuff.foo = (Stuff.foo + 1))
   conn.execute(stmt)
```