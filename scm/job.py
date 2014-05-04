#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

import subprocess
import sys
import os

sys.path.append("../")

import util.logRewrite as logRewrite
from model.jobInfo import JobInfo
from model.svnUrlInfo import SvnUrlInfo


def systemCommand(command):
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

if __name__ == '__main__':

    svnUrl = 'http://svn1.360buy-develop.com/pop/pop-order-work'
    #svnUrl = 'https://svn.sinaapp.com/foodcmd'
    job = JobInfo(svnUrl)
    # checkout svn code
    systemCommand(job.getSvnCheckOutCommand())

    # check svn log
    systemCommand(job.getSvnLogCommand())

    # rewrite log
    # logRewrite.rewriteLog(job.getSvnLogPath(), logRewrite.getAllNeedDeleteRevisions(job.getSvnLogPath()))

    # statsvn rewrite
    # systemCommand(job.getRewriteCommand())

    # statsvn delete
    # systemCommand(job.getDeleteCommand())