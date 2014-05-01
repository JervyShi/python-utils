#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

import unittest

from model.svnUrlInfo import SvnUrlInfo

class TestSvnUrlInfo(unittest.TestCase):

    def test_getSvnUrl(self):
        svnUrlInfos = SvnUrlInfo.get_svnUrl()
        for urlInfo in svnUrlInfos:
            print urlInfo
            self.assertIn('360buy-develop', urlInfo)

if __name__ == '__main__':
    unittest.main()
