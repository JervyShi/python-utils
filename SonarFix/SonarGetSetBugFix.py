# -*- coding: UTF-8 -*-
__author__ = 'bjshijianwei'

import re
import os
import sys

'''
模板：每个templates下的文件对应一个模版，
模板中定义的正则会匹配到需要修改的字符串
并根据替换规则替换
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
2和3只有在忽略大小写的情况下相等脚本才会处理
第二行为分隔符，务必是3个#，即：###
第三行到文件末尾为需要被替换后的代码，
私有属性名务必为template
'''
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

'''
用于读取templates目录下的模版配置文件
'''
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

'''
文件处理方法
会根据传入的路径递归寻找路径下所有的java文件，
并根据传入的模版匹配并修改文件
'''
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

'''
使用帮助
'''
def usage():
    print 'Usage: SonarGetSetBugFix.py [filePath]'
    print 'replace all get or set bugs that findbugs finded which is defined in templates folder'
    print 'Demo: ./SonarGetSetBugFix.py D:\\workspace\\trunk\\project-trunk\\project-domain\\'

if __name__ == '__main__':
    print sys.argv
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        usage()
        sys.exit(1)
    filePath = sys.argv[1]
    config = Config()
    templates = [Template(k,v) for k,v in config.list]
    handleFile(filePath, templates)
