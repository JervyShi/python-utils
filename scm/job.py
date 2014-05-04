#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

import subprocess
import sys
import os

sys.path.append("../")

import util.logRewrite as logRewrite
import util.userHtmlParser as userHtmlParser
from util.dateUtil import DateUtil
from model.jobInfo import JobInfo
from model.svnUrlInfo import SvnUrlInfo
from model.svnUsers import SvnUsers
from model.userDirectLines import AbsUserDirectLines, UserDirectLines, UserDirectLinesDel


def system_command(command):
    try:
        print command
        # pip = subprocess.check_output(command, shell=True)
        # print pip
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        out, err = process.communicate()
        print out, err
    except subprocess.CalledProcessError:
        pass


def store_user_direct_info(job, table_name):
    if job is not None and isinstance(job, JobInfo):
        svn_url_info = SvnUrlInfo.get_by_svn_url(job.svn_url)
        if svn_url_info is not None:
            path = job.get_rewrite_direct() if table_name == 'user_directory_linescode' else job.get_delete_direct()
            files = [f for f in os.listdir(path) if f.startswith('user_') and f.endswith(".html")]
            for f in files:
                user = f[5:-5]
                svn_user = SvnUsers.add(user)
                if svn_user is not None:
                    results = userHtmlParser.getTBodyContent(path + os.sep + f)
                    for data in results:
                        line = AbsUserDirectLines(0, svn_user_id=svn_user.id, svn_url_info_id=svn_url_info.id)
                        line.directory = data.get('directory')
                        line.changes = data.get('changes')
                        line.lines_of_code = data.get('lines_of_code')
                        line.lines_per_change = data.get('lines_per_change')
                        line.start_date = DateUtil.getMondayOfLastWeek()
                        line.end_date = DateUtil.getSundayOfLastWeek()
                        line.week = DateUtil.getLastWeekOfYear()
                        line.year = DateUtil.getYearOfLastWeek()
                        table_id = AbsUserDirectLines.add(line, table_name)
                        if table_id == 1:
                            print 'already exists', table_name, line
                        elif table_id > 1:
                            print 'add success', table_name, line
                        else:
                            print 'add error', table_name, line


if __name__ == '__main__':

    svnUrl = 'http://svn1.360buy-develop.com/pop/pop-order-work'
    #svnUrl = 'https://svn.sinaapp.com/foodcmd'
    job = JobInfo(svnUrl)
    print job.svn_url + 'process start'

    # checkout svn code
    print 'step 1: svn checkout'
    system_command(job.get_svn_check_out_command())

    # check svn log
    print 'step 2: svn log'
    system_command(job.get_svn_log_command())

    # rewrite log
    print 'step 3: rewrite log'
    logRewrite.rewriteLog(job.get_svn_log_path(), logRewrite.getAllNeedDeleteRevisions(job.get_svn_log_path()))

    # statsvn rewrite
    print 'step 4: statsvn analysis rewrite svn log'
    # system_command(job.get_rewrite_command())

    # statsvn delete
    print 'step 5: statsvn analysis delete svn log'
    # system_command(job.get_delete_command())

    # analysis html and put them into database
    print 'step 6: analysis html and put them into database'
    store_user_direct_info(job, 'user_directory_linescode')
    store_user_direct_info(job, 'user_directory_linescode_del')
