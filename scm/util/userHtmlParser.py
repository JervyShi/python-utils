__author__ = 'jervyshi'

import os

from bs4 import BeautifulSoup


def getTBodyContent(fileName):
    if os.path.isfile(fileName):
        soup = BeautifulSoup(open(fileName))
        results = []
        for tr in soup.table.tbody.find_all('tr'):
            json = {}
            json.setdefault('directory', tr.th.a.text)
            tds = tr.find_all('td')
            json.setdefault('changes', int(tds[0].text.split(' ')[0]))
            json.setdefault('lines_of_code', int(tds[1].text.split(' ')[0]))
            json.setdefault('lines_per_change', int(float(tds[2].text)))
            #print json
            results.append(json)
        #print results
        return results
    return []

if __name__ == '__main__':
    fileName = '/Users/jervyshi/Downloads/scm/resource/2014/pop_tuangou/16/excludeA+R/user_bjgejiangtao.html'
    print getTBodyContent(fileName)