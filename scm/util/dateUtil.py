#-*- coding:utf-8 -*-
__author__ = 'bjshijianwei'

from datetime import date
from datetime import timedelta


class DateUtil(object):

    @classmethod
    def getYear(cls):
        return date.today().year

    @classmethod
    def getWeekOfYear(cls):
        return date.today().isocalendar()[1]

    @classmethod
    def getLastWeekOfYear(cls):
        return (date.today() + timedelta(weeks=-1)).isocalendar()[1]

    @classmethod
    def getMondayOfLastWeek(cls):
        day = date.today()
        return day - timedelta(days=day.weekday()) + timedelta(days=0, weeks=-1)

    @classmethod
    def getSundayOfLastWeek(cls):
        day = date.today()
        return day - timedelta(days=day.weekday()) + timedelta(days=6, weeks=-1)

if __name__ == '__main__':
    print DateUtil.getYear()
    print DateUtil.getWeekOfYear()
    print DateUtil.getMondayOfLastWeek()
    print DateUtil.getSundayOfLastWeek()
    print DateUtil.getLastWeekOfYear()