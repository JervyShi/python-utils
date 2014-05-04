#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

import unittest

from scm.model.svnUrlInfo import SvnUrlInfo


class TestSvnUrlInfo(unittest.TestCase):

    def test_get(self):
        svn_url_info = SvnUrlInfo.get(1319)
        self.assertEqual('http://svn.360buy-develop.com/repos/branches', svn_url_info.svn_url)

    def test_get_by_svn_utl(self):
        svn_url_info = SvnUrlInfo.get_by_svn_url('http://svn.360buy-develop.com/repos/branches')
        self.assertEqual(1319, svn_url_info.id)

    def test_getSvnUrl(self):
        svn_url_list = SvnUrlInfo.get_all()
        for svn_url in svn_url_list:
            self.assertIn('360buy-develop', svn_url)

if __name__ == '__main__':
    unittest.main()
