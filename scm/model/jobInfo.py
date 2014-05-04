#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

import re
import os

import scm.config as Config
from scm.util.dateUtil import DateUtil


class JobInfo(object):
    REGEX = r'http\:\/\/(?P<svnKind>\w+\d?)\.360buy-develop\.com/(?P<svnLib>\w+)/(?P<svnDirect>.+)'
    EXCLUDE_A_R = 'excludeA+R'
    INCLUDE_A_R = 'includeA+R'

    def __init__(self, svn_url):
        self.svn_url = svn_url
        p = re.compile(JobInfo.REGEX, re.M)
        m = re.search(p, svn_url)
        self.svn_kind = 'svn1' if m.group('svnKind') == 'svn1' else 'svn'
        self.svn_lib = m.group('svnLib')
        self.svn_direct = m.group('svnDirect')
        self.log_name = 'logfile_%s.log' % self.svn_direct
        self.log_rewrite_name = 'logfile_%s.rewrite.log' % self.svn_direct
        self.log_delete_name = 'logfile_%s.delete.log' % self.svn_direct

    def get_direct_path(self):
        """directPath
        demo: C:\resource\2014\svn1\cdrd_jos\17
        """
        return """%s%s%s%s%s%s%s_%s%s%s""" % (Config.DIRECTORY_PREFIX, os.sep, str(DateUtil.getYear()), os.sep,
               self.svn_kind, os.sep, self.svn_lib, self.svn_direct,
               os.sep, str(DateUtil.getLastWeekOfYear()))

    def get_check_out_path(self):
        """checkOutPath
        demo: C:\resource\2014\svn1\cdrd_jos\17\checkout
        """
        return self.get_direct_path() + os.sep + 'checkout'

    def get_svn_log_path(self):
        return self.get_check_out_path() + os.sep + self.log_name

    def get_svn_rewrite_log_path(self):
        return self.get_check_out_path() + os.sep + self.log_rewrite_name

    def get_svn_delete_log_path(self):
        return self.get_check_out_path() + os.sep + self.log_delete_name

    def get_svn_check_out_command(self):
        return 'svn checkout --depth immediates %s %s' % (self.svn_url, self.get_check_out_path())

    def get_svn_log_command(self):
        """svn log command
        demo: svn log -r {2014-4-21}:{2014-4-27} -v --xml>logfile_jos.log
        """
        return 'svn log %s -r {%s}:{%s} -v --xml>%s' % (
            self.svn_url, DateUtil.getMondayOfLastWeek(), DateUtil.getSundayOfLastWeek(),
            self.get_svn_log_path())

    def get_rewrite_command(self):
        return 'java -jar %s %s %s -charset gb2312 -output-dir %s' % (
            Config.STATSVN_PATH, self.get_svn_rewrite_log_path(), self.get_check_out_path(),
            self.get_rewrite_direct())

    def get_delete_command(self):
        return 'java -jar %s %s %s -charset gb2312 -output-dir %s' % (
            Config.STATSVN_PATH, self.get_svn_delete_log_path(), self.get_check_out_path(),
            self.get_delete_direct())

    def get_rewrite_direct(self):
        return '%s%s%s' % (self.get_direct_path(), os.sep, JobInfo.EXCLUDE_A_R)

    def get_delete_direct(self):
        return '%s%s%s' % (self.get_direct_path(), os.sep, JobInfo.INCLUDE_A_R)

if __name__ == '__main__':
    job = JobInfo('http://svn1.360buy-develop.com/cdrd/jos')
    print job.get_direct_path()
    print job.get_check_out_path()
    print job.get_svn_check_out_command()
    print job.get_svn_log_command()
    print job.get_rewrite_command()
    print job.get_delete_command()

