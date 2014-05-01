#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

import argparse
import sys
import re
import xml.etree.ElementTree as ET


def getAllNeedDeleteRevisions(filePath):
    print 'analysing revisions needs to be deleted'
    revisionList = []
    tree = ET.parse(filePath)
    root = tree.getroot()
    for logentry in root.iter('logentry'):
        pathCount = 0
        pathACount = 0
        pathRCount = 0

        for path in logentry.iter('path'):
            pathCount += 1
            if path.get('action') == 'A':
                pathACount += 1
            if path.get('action') == 'R':
                pathRCount += 1

        if pathCount is not 0:
            if pathCount == pathACount or pathCount == pathRCount:
                revisionList.append(logentry.get('revision'))
    return revisionList


def rewriteLog(filePath, revisionList):
    print 'deleting revisions ...'
    rewriteFilePath = filePath[:-4] + '.rewrite.log'
    deleteFilePath = filePath[:-4] + '.delete.log'
    with open(filePath, 'r') as f:
        with open(rewriteFilePath, 'w') as w:
            with open(deleteFilePath, 'w') as d:
                content = f.read()
                regex = '(<logentry\s+revision="(' + '|'.join(revisionList) + ')">((?!</logentry>).*\s*)*</logentry>)'
                print 'revision', revisionList, 'has been deleted'
                p = re.compile(regex, re.M)
                mList = re.findall(p, content)
                print 'writing delete items to', deleteFilePath
                d.write('<?xml version="1.0"?>\r\n<log>\r\n')
                for text in mList:
                    d.write(text[0]+'\r\n')
                d.write('</log>')
                print 'write delete items success, filePath:', deleteFilePath
                content = re.sub(p, '', content)
                print 'rewriting file to', rewriteFilePath
                w.write(content)
                print 'rewrite success, filePath:', rewriteFilePath


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("-f", '--filePath', action="store", help="which file need process")
    args = parse.parse_args(sys.argv[1:])
    filePath = args.filePath
    if filePath is None:
        parse.print_help()
    else:
        rewriteLog(filePath, getAllNeedDeleteRevisions(filePath))
