#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

from scm.store import db_conn

from MySQLdb import IntegrityError


class SvnUsers(object):
    def __init__(self, id, svn_user=None):
        self.id = id
        self.svn_user = svn_user

    @classmethod
    def get(cls, id):
        cursor = db_conn.execute("""SELECT id, svn_user
            FROM svn_users WHERE id=%s""", (id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            u = cls(row[0])
            u.svn_user = str(row[1])
            return u
        return None

    @classmethod
    def get_by_svn_user(cls, svn_user):
        if svn_user is None:
            return None
        cursor = db_conn.execute("""SELECT id, svn_user
            FROM svn_users WHERE svn_user=%s""", (svn_user,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            u = cls(row[0])
            u.svn_user = str(row[1])
            return u
        return None

    @classmethod
    def add(cls, svn_user=None):
        cursor = None
        user = None
        try:
            if svn_user:
                user = cls.get_by_svn_user(svn_user)
            if user is None:
                cursor = db_conn.execute("""INSERT INTO svn_users (svn_user)  VALUES (%s)""", (svn_user,))
                user_id = cursor.lastrowid
                db_conn.commit()
                user = cls.get(user_id)
        except IntegrityError:
            db_conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return user



