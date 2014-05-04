#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

from scm.store import db_conn


class SvnUrlInfo(object):

    def __init__(self, id, svn_url=None):
        self.id = id
        self.svn_url = svn_url

    @classmethod
    def get(cls, id):
        cursor = db_conn.execute("""SELECT id, svn_url FROM svn_url_info WHERE id=%s""", (id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            su = SvnUrlInfo(row[0])
            su.svn_url = str(row[1])
            return su
        return None

    @classmethod
    def get_by_svn_url(cls, svn_url):
        cursor = db_conn.execute("""SELECT id, svn_url FROM svn_url_info WHERE svn_url=%s""", (svn_url,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            su = SvnUrlInfo(row[0])
            su.svn_url = str(row[1])
            return su
        return None

    @classmethod
    def add(cls, svn_url):
        svn_url_info = cls.get_by_svn_url(svn_url)
        if svn_url_info is None:
            cursor = db_conn.execute("""insert into svn_url_info (svn_url) values(%s)""", (svn_url,))
            db_conn.commit()
            cursor.close()
            svn_url_info = cls.get_by_svn_url(svn_url)
        return svn_url_info

    @classmethod
    def get_all(cls):
        cursor = db_conn.execute('''SELECT svn_url FROM svn_url_info''')
        rows = cursor.fetchall()
        return [x[0] for x in rows]
