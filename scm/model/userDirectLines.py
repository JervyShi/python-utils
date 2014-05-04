#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

from scm.store import db_conn

from MySQLdb import IntegrityError


class AbsUserDirectLines(object):
    def __repr__(self):
        return """<id=%s, svn_user_id=%s, svn_url_info=%s, lines_of_code=%s, changes=%s,
                lines_per_change=%s, directory=%s, start_date=%s, end_date=%s, week=%s, year=%s>""" % (
            self.id, self.svn_user_id, self.svn_url_info_id, self.lines_of_code, self.changes,
            self.lines_per_change, self.directory, self.start_date, self.end_date, self.week, self.year
        )

    __str__ = __repr__

    def __init__(self, id, svn_user_id=None, svn_url_info_id=None, lines_of_code=None,
                 changes=None, lines_per_change=None, directory=None, start_date=None,
                 end_date=None, week=None, year=None):
        self.id = id
        self.svn_user_id = svn_user_id
        self.svn_url_info_id = svn_url_info_id
        self.lines_of_code = lines_of_code
        self.changes = changes
        self.lines_per_change = lines_per_change
        self.directory = directory
        self.start_date = start_date
        self.end_date = end_date
        self.week = week
        self.year = year

    @classmethod
    def count(cls, udl, table_name=None):
        cursor = None
        if udl is not None and isinstance(udl, AbsUserDirectLines):
            cursor = db_conn.execute("""SELECT count(1)
                                    FROM """ + table_name + """ WHERE svn_user_id=%s and svn_url_info_id=%s
                                    and directory=%s and start_date=%s and end_date=%s and week=%s and year=%s""",
                                    (udl.svn_user_id, udl.svn_url_info_id,
                                     udl.directory, udl.start_date, udl.end_date, udl.week, udl.year))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return row[0]
        return None


    @classmethod
    def add(cls, udl, table_name=None):
        cursor = None
        table_id = None
        if udl is not None and isinstance(udl, AbsUserDirectLines):
            try:
                count = cls.count(udl, table_name)
                if count > 0:
                    table_id = count
                else:
                    cursor = db_conn.execute('''insert into ''' + table_name +
                                             ''' (svn_user_id,svn_url_info_id,Lines_of_Code,Changes,Lines_per_Change,
                                             Directory,start_date,end_date,week,year)
                                             values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                             (udl.svn_user_id, udl.svn_url_info_id, udl.lines_of_code,
                                              udl.changes, udl.lines_per_change, udl.directory,
                                              udl.start_date, udl.end_date,
                                              udl.week, udl.year))
                    table_id = cursor.lastrowid
                    db_conn.commit()
            except IntegrityError:
                db_conn.rollback()
            finally:
                if cursor:
                    cursor.close()
        return table_id


class UserDirectLines(AbsUserDirectLines):
    def __init__(self, id, svn_user_id=None, svn_url_info_id=None, lines_of_code=None, changes=None,
                 lines_per_change=None, directory=None, start_date=None, end_date=None, week=None, year=None):
        super(UserDirectLines, self).__init__(id, svn_user_id, svn_url_info_id, lines_of_code, changes,
                                              lines_per_change, directory, start_date, end_date, week, year)

    @classmethod
    def count(cls, udl, table_name=None):
        return super(UserDirectLines, cls).count(udl, 'user_directory_linescode')

    @classmethod
    def add(cls, udl, table_name=None):
        return super(UserDirectLines, cls).add(udl, 'user_directory_linescode')


class UserDirectLinesDel(AbsUserDirectLines):
    def __init__(self, id, svn_user_id=None, svn_url_info_id=None, lines_of_code=None, changes=None,
                 lines_per_change=None, directory=None, start_date=None, end_date=None, week=None, year=None):
        super(UserDirectLinesDel, self).__init__(id, svn_user_id, svn_url_info_id, lines_of_code, changes,
                                                 lines_per_change, directory, start_date, end_date, week, year)

    @classmethod
    def count(cls, udl, table_name=None):
        return super(UserDirectLinesDel, cls).count(udl, 'user_directory_linescode_del')

    @classmethod
    def add(cls, udl, table_name=None):
        return super(UserDirectLinesDel, cls).add(udl, 'user_directory_linescode_del')
