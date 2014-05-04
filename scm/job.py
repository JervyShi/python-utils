#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

import subprocess
import sys
import os
import traceback
import logging
import logging.config

sys.path.append("../")

import util.logRewrite as logRewrite
import util.userHtmlParser as userHtmlParser
from util.dateUtil import DateUtil
from model.jobInfo import JobInfo
from model.svnUrlInfo import SvnUrlInfo
from model.svnUsers import SvnUsers
from model.userDirectLines import AbsUserDirectLines

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("main")


def system_command(command):
    try:
        logger.debug(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, universal_newlines=True)
        out, err = process.communicate()
        logger.debug('out: %s error: %s' % (out, err))
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
                            logger.debug('already exists %s %s' % (table_name, line))
                        elif table_id > 1:
                            logger.debug('add success %s %s' % (table_name, line))
                        else:
                            logger.debug('add error %s %s' % (table_name, line))


def main():

    logger.info('%s %s {%s} - {%s} job end' % (
        DateUtil.getYearOfLastWeek(), DateUtil.getLastWeekOfYear(),
        DateUtil.getMondayOfLastWeek(), DateUtil.getSundayOfLastWeek()))
    svn_url_list = SvnUrlInfo.get_all()
    # svn_url_list = ['http://svn1.360buy-develop.com/pop/pop-order-work']
    for svn_url in svn_url_list:
        try:
            job = JobInfo(svn_url)
            logger.info('%s process start' % (job.svn_url,))

            # checkout svn code
            logger.info('step 1: svn checkout')
            system_command(job.get_svn_check_out_command())

            # check svn log
            logger.info('step 2: svn log')
            system_command(job.get_svn_log_command())

            # rewrite log
            logger.info('step 3: rewrite log')
            logRewrite.rewriteLog(job.get_svn_log_path(), logRewrite.getAllNeedDeleteRevisions(job.get_svn_log_path()))

            # statsvn rewrite
            logger.info('step 4: statsvn analysis rewrite svn log')
            system_command(job.get_rewrite_command())

            # statsvn delete
            logger.info('step 5: statsvn analysis delete svn log')
            system_command(job.get_delete_command())

            # analysis html and put them into database
            logger.info('step 6: analysis html and put them into database')
            store_user_direct_info(job, 'user_directory_linescode')
            store_user_direct_info(job, 'user_directory_linescode_del')
            logger.info('%s process end' % svn_url)
        except Exception:
            logger.error('%s process error' % svn_url)
            logger.error(traceback.format_exc())
    logger.info('%s %s {%s} - {%s} job end' % (
        DateUtil.getYearOfLastWeek(), DateUtil.getLastWeekOfYear(),
        DateUtil.getMondayOfLastWeek(), DateUtil.getSundayOfLastWeek()))

if __name__ == '__main__':
    main()