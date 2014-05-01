#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

from store import db_conn

from MySQLdb import IntegrityError


class SvnUsers(object):
    def __init__(self, id):
        self.id = id
        self.svnUser = None

    @classmethod
    def get(cls, id):
        cursor = db_conn.execute("""SELECT id, svn_user
            FROM svn_users WHERE id=%s""" % id)
        row = cursor.fetchone()
        cursor.close()
        if row:
            u = cls(row[0])
            u.svnUser = str(row[1])
            return u
        return None

    @classmethod
    def get_by_svnUser(cls, svnUser):
        if svnUser is None:
            return None
        cursor = db_conn.execute("""SELECT id, svn_user
            FROM svn_users WHERE svn_user=%s""" % svnUser)
        row = cursor.fetchone()
        cursor.close()
        if row:
            u = cls(row[0])
            u.svnUser = str(row[1])
            return u
        return None

    @classmethod
    def add(cls, svnUser=None):
        cursor = None
        user = None
        try:
            if svnUser:
                user = cls.get_by_svnUser(svnUser)
            if user is None:
                cursor = db_conn.execute("""INSERT INTO svn_users (svn_user)  VALUES (%s)""" % svnUser)
                user_id = cursor.lastrowid
                db_conn.commit()
                user = cls.get(user_id)
        except IntegrityError:
            db_conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return user



