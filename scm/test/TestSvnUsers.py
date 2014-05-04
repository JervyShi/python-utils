#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

import unittest

from scm.model.svnUsers import SvnUsers


class TestSvnUsers(unittest.TestCase):

    def test_get(self):
        u = SvnUsers.get(647)
        self.assertEqual(u.svn_user, 'bjshijianwei')

    def test_getBySvnUser(self):
        u = SvnUsers.get_by_svn_user('bjshijianwei')
        self.assertEqual(u.id, 647)

    def test_add(self):
        u = SvnUsers.add('shijianwei')
        self.assertEqual(u.svn_user, 'shijianwei')

if __name__ == '__main__':
    unittest.main()