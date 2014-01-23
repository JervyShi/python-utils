# -*- coding: UTF-8 -*-
__author__ = 'bjshijianwei'

import re
import os

class Template:
    def __init__(self, regex, template):
        self.regex = regex
        self.template = template

    def firstUpper(self, name):
        length = len(name)
        if length == 0:
            return ''
        if length == 1:
            return name.upper()
        return name[0:1].upper() + name[1:length]

    def bugFix(self, text):
        p = re.compile(self.regex, re.M)
        mList = re.findall(p, text)
        for func, upName, name in mList:
            if upName.lower() == name.lower():
                temp = self.template.replace('Template', self.firstUpper(name))
                temp = temp.replace('template', name)
                text = text.replace(func, temp)
        return text

class Config:
    def __init__(self):
        self.list = []
        dirPath = '.\\templates'
        if os.path.isdir(dirPath):
            fList = [dirPath + os.sep+x for x in os.listdir(dirPath)]
            for f in fList:
                with open(f, 'r') as file:
                    content = file.read()
                    kvs = content.split('###')
                    self.list.append((kvs[0].strip(), kvs[1].strip()))

    def getList(self):
        return self.list

def handleFile(filePath, templates):
    if filePath.find('.svn') > 0:
        return
    if filePath.find('.idea') > 0:
        return
    if os.path.isdir(filePath):
        filelist = [filePath+os.sep+x for x in os.listdir(filePath)]
        for x in filelist:
            handleFile(x, templates)
    if os.path.isfile(filePath):
        if filePath.find('.java') > 0:
            with open(filePath, 'r') as f:
                text = f.read()
                textCompare = text
            for temp in templates:
                text = temp.bugFix(text)
            if text != textCompare:
                with open(filePath, 'w') as f:
                    f.write(text)
                    print 'success', filePath

if __name__ == '__main__':
    config = Config()
    templates = [Template(k,v) for k,v in config.list]
    handleFile('D:\\workspace\\trunk\\pop-admin-order-trunk\\pop-order-common-domain\\src\\main\\java\\com\\jd\\pop\\domain\\promotion', templates)
