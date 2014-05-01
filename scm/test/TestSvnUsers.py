#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

import unittest

from model.svnUsers import SvnUsers

class TestSvnUsers(unittest.TestCase):

    def test_get(self):
        u = SvnUsers.get(647)
        self.assertEqual(u.svnUser, 'bjshijianwei')

    def test_getBySvnUser(self):
        u = SvnUsers.get_by_svnUser('bjshijianwei')
        self.assertEqual(u.id, 647)

    def test_add(self):
        u = SvnUsers.add('shijianwei')
        self.assertEqual(u.svnUser, 'shijianwei')

if __name__ == '__main__':
    unittest.main()