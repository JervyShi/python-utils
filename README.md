python-utils
============

自写自用python小工具

###1、logDownload.py
@desc:
通过urllib2下载相同域名不同服务器地址上的日志文件

@usage:配置config.cfg文件(支持注释:#开头行会忽略)

服务器ip列表配置如：'ipList:192.168.1.100,192.168.1.101' (多ip用英文逗号分隔)

	ipList:192.168.1.100,192.168.1.101

域名配置：'domain:jervyshi.me' (此配置唯一)

	domain:jervyshi.me

需下载日志文件名：'logNameList:debug.log' (多日志文件用英文逗号
分隔)

	logNameList:debug.log

链接中间串:'concat:/logs/' (此串用于拼装完整链接，为空使用默认值)

	concat:/logs/

日志文件输出路径：'outPath:' (为空则使用当前路径)

	outPath:

@demo 

查看帮助

	./logDownload.py -h

使用配置文件

	./logDownlaod.py -c config.cfg
