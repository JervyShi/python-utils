#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

from store import db_conn


class SvnUrlInfo(object):

    def __init__(self, id, svnUrl):
        self.id = id
        self.svnUrl = svnUrl

    @classmethod
    def get_svnUrl(cls):
        cursor = db_conn.execute('''SELECT svn_url FROM svn_url_info''')
        rows = cursor.fetchall()
        return [x[0] for x in rows]
