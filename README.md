# SRTP
### 见[后端配置.pdf]

## 补充关于mysql的一些配置问题
`mysql -uxxx -pxxx`报错`ERROR 2003 (HY000): Can't connect to MySQL server on 'localhost:3306' (10061)`
### 解决方式
输入`mysqld --console`命令，新开窗口重新连接`mysql -uxxx -pxxx`即可成功连接
