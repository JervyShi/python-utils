#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

import unittest

from model.userDirectLines import UserDirectLines, UserDirectLinesDel, AbsUserDirectLines


class TestUserDirectLines(unittest.TestCase):

    def test_userDirectLines(self):
        udl = UserDirectLines(0, 670, 1865, 2, 1, 2, 'branches/20140319_chayi/pop-store-service/src/main/java/com/jd/pop/store/service/timetask/', '2014-03-31', '2014-04-06', 14, 2014)
        id = UserDirectLines.add(udl)
        print id
        self.assertGreater(id, 0)

    def test_userDirectLinesDel(self):
        udl = UserDirectLinesDel(0, 670, 1865, 2, 1, 2, 'branches/20140319_chayi/pop-store-service/src/main/java/com/jd/pop/store/service/timetask/', '2014-03-31', '2014-04-06', 14, 2014)
        id = UserDirectLinesDel.add(udl)
        print id
        self.assertGreater(id, 0)

if __name__ == '__main__':
    unittest.main()