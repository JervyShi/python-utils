#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

import subprocess
import sys
import os

sys.path.append("../")

import util.logRewrite as logRewrite
from model.jobInfo import JobInfo
from model.svnUrlInfo import SvnUrlInfo


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

def store_user_direct_info(job):
    if job is not None and isinstance(job, JobInfo):
        svn_url_info = SvnUrlInfo.get_by_svn_url(job.svn_url)


if __name__ == '__main__':

    svnUrl = 'http://svn1.360buy-develop.com/pop/pop-order-work'
    #svnUrl = 'https://svn.sinaapp.com/foodcmd'
    job = JobInfo(svnUrl)
    # checkout svn code
    system_command(job.getSvnCheckOutCommand())

    # check svn log
    system_command(job.getSvnLogCommand())

    # rewrite log
    # logRewrite.rewriteLog(job.getSvnLogPath(), logRewrite.getAllNeedDeleteRevisions(job.getSvnLogPath()))

    # statsvn rewrite
    # system_command(job.getRewriteCommand())

    # statsvn delete
    # system_command(job.getDeleteCommand())
