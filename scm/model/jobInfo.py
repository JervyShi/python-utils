#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

import re
import os

import config
from util.dateUtil import DateUtil


class JobInfo(object):
    REGEX = r'http\:\/\/(?P<svnKind>\w+\d?)\.360buy-develop\.com/(?P<svnLib>\w+)/(?P<svnDirect>.+)'
    EXCLUDEA_R = 'excludeA+R'
    INCLUDEA_R = 'includeA+R'

    def __init__(self, svnUrl):
        self.svnUrl = svnUrl
        p = re.compile(JobInfo.REGEX, re.M)
        m = re.search(p, svnUrl)
        self.svnKind = 'svn1' if m.group('svnKind') == 'svn1' else 'svn'
        self.svnLib = m.group('svnLib')
        self.svnDirect = m.group('svnDirect')
        self.logName = 'logfile_%s.log' % self.svnDirect
        self.logRewriteName = 'logfile_%s.rewrite.log' % self.svnDirect
        self.logDeleteName = 'logfile_%s.delete.log' % self.svnDirect

    def getDirectPath(self):
        """directPath
        demo: C:\resource\2014\svn1\cdrd_jos\17
        """
        return config.DIRECTORY_PREFIX + os.sep + str(DateUtil.getYear()) + os.sep \
               + self.svnKind + os.sep + self.svnLib + '_' + self.svnDirect \
               + os.sep + str(DateUtil.getWeekOfYear())

    def getCheckOutPath(self):
        """checkOutPath
        demo: C:\resource\2014\svn1\cdrd_jos\17\checkout
        """
        return self.getDirectPath() + os.sep + 'checkout'

    def getSvnLogPath(self):
        return self.getCheckOutPath() + os.sep + self.logName

    def getSvnRewriteLogPath(self):
        return self.getCheckOutPath() + os.sep + self.logRewriteName

    def getSvnDeleteLogPath(self):
        return self.getCheckOutPath() + os.sep + self.logDeleteName

    def getSvnCheckOutCommand(self):
        #return ['svn', 'checkout', '--depth', 'immediates', str(self.svnUrl), str(self.getCheckOutPath())]
        return 'svn checkout --depth immediates %s %s' % (self.svnUrl, self.getCheckOutPath())

    def getSvnLogCommand(self):
        """svn log command
        demo: svn log -r {2014-4-21}:{2014-4-27} -v --xml>logfile_jos.log
        """
        return 'cd %s && svn log -r {%s}:{%s} -v --xml>logfile_%s.log' % (self.getCheckOutPath(),
            DateUtil.getMondayOfLastWeek(), DateUtil.getSundayOfLastWeek(), self.svnDirect)

    def getRewriteCommand(self):
        return 'java -jar %s %s %s -charset gb2312 -output-dir %s' % (
            config.STATSVN_PATH, self.getSvnRewriteLogPath(), self.getCheckOutPath(),
            self.getDirectPath() + os.sep + JobInfo.EXCLUDEA_R)

    def getDeleteCommand(self):
        return 'java -jar %s %s %s -charset gb2312 -output-dir %s' % (
            config.STATSVN_PATH, self.getSvnDeleteLogPath(), self.getCheckOutPath(),
            self.getDirectPath() + os.sep + JobInfo.INCLUDEA_R)


if __name__ == '__main__':
    job = JobInfo('http://svn1.360buy-develop.com/cdrd/jos')
    print job.getDirectPath()
    print job.getCheckOutPath()
    print job.getSvnCheckOutCommand()
    print job.getSvnLogCommand()
    print job.getRewriteCommand()
    print job.getDeleteCommand()

