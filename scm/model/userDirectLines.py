#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

from store import db_conn

from MySQLdb import IntegrityError


class AbsUserDirectLines(object):
    def __init__(self, id, svnUserId=None, svnUrlInfoId=None, linesOfCode=None,
                 changes=None, linesPerChange=None, directory=None, startDate=None,
                 endDate=None, week=None, year=None):
        self.id = id
        self.svnUserId = svnUserId
        self.svnUrlInfoId = svnUrlInfoId
        self.linesOfCode = linesOfCode
        self.changes = changes
        self.linesPerChange = linesPerChange
        self.directory = directory
        self.startDate = startDate
        self.endDate = endDate
        self.week = week
        self.year = year

    @classmethod
    def add(cls, udl, tableName=None):
        cursor = None
        table_id = None
        if udl is not None and isinstance(udl, AbsUserDirectLines):
            try:
                cursor = db_conn.execute('''insert into ''' + tableName + ''' (svn_user_id,svn_url_info_id,Lines_of_Code,Changes,Lines_per_Change,Directory,start_date,end_date,week,year)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', [udl.svnUserId, udl.svnUrlInfoId, udl.linesOfCode,
                                         udl.changes, udl.linesPerChange, udl.directory, udl.startDate, udl.endDate,
                                         udl.week, udl.year])
                table_id = cursor.lastrowid
                db_conn.commit()
            except IntegrityError:
                db_conn.rollback()
            finally:
                if cursor:
                    cursor.close()
        return table_id


class UserDirectLines(AbsUserDirectLines):
    def __init__(self, id, svnUserId=None, svnUrlInfoId=None, linesOfCode=None, changes=None, linesPerChange=None,
                 directory=None, startDate=None, endDate=None, week=None, year=None):
        super(UserDirectLines, self).__init__(id, svnUserId, svnUrlInfoId, linesOfCode, changes, linesPerChange,
                                              directory, startDate, endDate, week, year)

    @classmethod
    def add(cls, udl, tableName=None):
        return super(UserDirectLines, cls).add(udl, 'user_directory_linescode')


class UserDirectLinesDel(AbsUserDirectLines):
    def __init__(self, id, svnUserId=None, svnUrlInfoId=None, linesOfCode=None, changes=None, linesPerChange=None,
                 directory=None, startDate=None, endDate=None, week=None, year=None):
        super(UserDirectLinesDel, self).__init__(id, svnUserId, svnUrlInfoId, linesOfCode, changes, linesPerChange,
                                                 directory, startDate, endDate, week, year)

    @classmethod
    def add(cls, udl, tablName=None):
        return super(UserDirectLinesDel, cls).add(udl, 'user_directory_linescode_del')
