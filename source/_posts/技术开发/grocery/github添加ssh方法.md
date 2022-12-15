## Windows

### 生成一个新的SSH key

    打开 git bash
    输入 
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
     

    输入一个文件名，默认是id_rsa，该步骤可直接选择默认即可。（多用户的可能要设置另一个名字，以防止冲突）
    输入密码，同上可以选择默认即可。

### 将新生成的SSH key添加到github

    复制key到粘贴板

    github设置中添加ssh key

## Linux

### 生成密钥

`ssh-keygen -t rsa -C "11706@sangfor.com"` 根据提示完成下一步

### 添加 SSH key到 ssh-agent

`eval $(ssh-agent -s)` 确保ssh-agent工作

`ssh-add ~/.ssh/id_rsa` 将 ssh 私钥添加到 ssh 代理中

### 将新生成的SSH key添加到github

复制key到粘贴板

github设置中添加ssh key

### 连接测试
`ssh -T git@github.com`
```angular2html
$ ssh -T git@github.com
Hi xxx! You've successfully authenticated, but GitHub does not provide shell access.
```

如果某天突然报错
```angular2html
kex_exchange_identification: Connection closed by remote host
Connection closed by 20.205.243.166 port 22
fatal: Could not read from remote repository.
```
可以尝试重新运行一次 `ssh -T git@github.com` 命令
