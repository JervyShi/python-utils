# -*- coding:utf-8 -*-
__author__ = 'jervyshi'

import chardet
import os


class Change(object):

    def __init__(self, readPath, writePath, fromEncoding, toEncoding):
        self.readPath = readPath
        self.writePath = writePath
        self.fromEncoding = fromEncoding
        self.toEncoding = toEncoding

    def change(self, file_path):
        if file_path.find('.svn') > 0:
            return
        if file_path.find('.idea') > 0:
            return
        if os.path.isfile(file_path):
            self.copy_file(file_path)
        elif os.path.isdir(file_path):
            to_path = self.get_to_path(file_path)
            if not os.path.exists(to_path):
                os.mkdir(to_path)
            file_list = [file_path+os.sep+x for x in os.listdir(file_path)]
            for x in file_list:
                self.change(x)

    def get_to_path(self, file_path):
        return file_path.replace(self.readPath, self.writePath)

    def copy_file(self, file_path):
        to_path = self.get_to_path(file_path)
        with open(file_path, 'r') as f:
            content = f.read()
            coding = chardet.detect(content)
            with open(to_path, 'w') as w:
                if coding['encoding'].lower() == self.fromEncoding:
                    print 'path:%s,encoding change' % file_path
                    w.write(content.decode(self.fromEncoding).encode(self.toEncoding))
                else:
                    print 'copy:%s, encoding:%s' % (file_path, coding['encoding'])
                    w.write(content)

    def work(self):
        self.change(self.readPath)


if __name__ == '__main__':
    change = Change('/home/jervyshi/workspace/branches/pop-order-work20140702-encoding-change', '/home/jervyshi/workspace/branches/change/pop-order-work20140702-encoding-change', 'gb2312', 'utf-8')
    change.work()