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

###2、SonarGetSetBugFix.py
**诞生背景：**

上了持续集成之后，持续集成中Findbugs插件把老项目中的各种bug都找了出来，其中基本所有的java实体bean全部中枪，那些IDE自动生成的get set方法，大多私有属性是包装类型的基本全报bug，如Date，String[]等。此问题产生于包装类型传入的是引用，传入后可能会在外部被更改掉，因此这是不安全的，解决办法也很简单，判空后克隆就好。介于人工修改工作量大且易出错便诞生了此脚本。

**脚本组成**

主脚本文件：SonarGetSetBugFix.py

模板文件：templates下的所有文件

**使用说明**

    Usage:  SonarGetSetBugFix.py [filePath]
    Demo:   ./SonarGetSetBugFix.py D:\\workspace\\trunk\\project-trunk\\project-domain\\

**模板说明**

模板中定义的正则会匹配到需要修改的字符串并根据替换规则替换

模版文件示例：

    (public\s+void\s+set(\w+)\(\s*Date\s+(?P<name>\w+)\)\s+{\s+this.(?P=name)\s+=\s+(?P=name);\s+})
    ###
        public void setTemplate(Date template) {
            if (template == null) {
                this.template = null;
            } else {
                this.template = (Date) template.clone();
            }
        }

第一行为正则，从此正则中应能提取出三组数据：

1. 完整的function
2. get or set后的方法名
3. 私有属性名

注意点：

2和3只有在忽略大小写的情况下相等脚本才会处理

第二行为分隔符，务必是3个#，即：###

第三行到文件末尾为需要被替换后的代码，私有属性名务必为template

templates目录中新增模版文件后无需修改程序
