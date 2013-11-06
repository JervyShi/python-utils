# -*- coding: UTF-8 -*-
'''
filename:logDownload.py
@desc:
通过urllib2下载相同域名不同服务器地址上的日志文件

@usage:
配置config.cfg文件(支持注释:#开头行会忽略)
服务器ip列表配置如：'ipList:192.168.1.100,192.168.1.101' (多ip用英文逗号分隔)
域名配置：'domain:jervyshi.me' (此配置唯一)
需下载日志文件名：'logNameList:debug.log' (多日志文件用英文逗号分隔)
链接中间串:'concat:/logs/' (此串用于拼装完整链接，为空使用默认值)
日志文件输出路径：'outPath:' (为空则使用当前路径)
'''
import os
import sys
import time
import urllib2

'''
配置类每个实例对应一个下载文件
'''
class Config:
    def __init__(self, ip, domain, logName, concat='/logs/', outPath=os.getcwd()):
        self.ip = ip
        self.domain = domain
        self.logName = logName
        self.concat = concat
        self.outPath = outPath

    def getUrl(self):
        return 'http://' + self.ip + self.concat + self.logName

    def getPath(self):
        return self.outPath + os.sep + time.strftime('%Y%m%d') + os.sep + self.domain

    def getFilePath(self):
        return self.getPath() + os.sep + self.ip + self.logName

'''
下载单个日志文件
'''
def urlDownload(conf):
    try:
        start = time.time()
        print conf.domain + ' ' + conf.ip + ' ' + conf.logName + ' download start...'
        req = urllib2.Request(conf.getUrl())
        req.add_header('Host', conf.domain)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0')
        if not os.path.exists(conf.getPath()):
            os.makedirs(conf.getPath())
        r = urllib2.urlopen(req)
        with open(conf.getFilePath(), 'w') as f:
            f.write(r.read())
        print conf.domain + ' ' + conf.ip + ' ' + conf.logName + ' download success cost: ' + str(int(1000 * (time.time() - start))) + ' ms'
    except Exception, e:
        print 'request error'


'''
使用帮助
'''
def usage():
    print 'Usage: logDownload.py [option] [file]'
    print 'Download log files from different hosts with same domain'
    print '  -h --help       usage help'
    print '  -c --config     set configuration file'
    print ''
    print 'Demo: ./logDownload.py -c config.cfg'

if __name__ == '__main__':
    start = time.time()
    dict = {}
    cfg = 'config.cfg'
    if len(sys.argv) > 3:
        usage()
        sys.exit(1)
    if len(sys.argv) == 2:
        argv = sys.argv[1]
        if argv == '-h' or argv == '--help':
            usage()
            sys.exit(1)
        if argv == '-c' or argv == '--config':
            cfg = 'config.cfg'
    if len(sys.argv) == 3:
        argvs = [sys.argv[1], sys.argv[2]]
        if argvs[0] == '-c' or argvs[0] == '--config':
            cfg = argvs[1]
    with open(cfg, 'r') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('#'):
                k, v = line.split(':')
                dict[k] = v
    ipList = dict.get('ipList').split(',')
    domain = dict.get('domain')
    logNameList = dict.get('logNameList').split(',')
    concat = dict.get('concat')
    outPath = dict.get('outPathList')
    if not outPath:
        outPath = os.getcwd()
    conf = Config('', domain, '', concat, outPath)
    for ip in ipList:
        conf.ip = ip
        for logName in logNameList:
            conf.logName = logName
            urlDownload(conf)
    print 'All file download success. cost: ' + str(int(1000 * (time.time() - start))) + ' ms'
