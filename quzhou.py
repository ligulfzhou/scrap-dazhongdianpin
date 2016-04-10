import time
import urllib.request
from urllib.request import Request, urlopen
import pymongo
from bs4 import BeautifulSoup


quzhou = pymongo.MongoClient('127.0.0.1:27017').quzhou
# util = pymongo.MongoClient('127.0.0.1:27017').util
#
# def mongo_uid(dbname, colname):
#     coll = util.sequence
#     now = round(time.time() * 1000)
#     update = {'$inc': {'seq': 1}, '$set': {'modified': now}}
#     ret = coll.find_and_modify({'dbname': dbname, 'colname': colname}, update, new=True, fields={'_id': 0, 'seq': 1})
#     return ret['seq']


#  name:   ***,    mobile: ***,    category: ***
def insert_into_mongodb(dbname, name, categoty, mobile):
    # data_id = mongo_uid(dbname, 'store')
    # xihuqu.store.insert({'id': data_id, 'name': name, 'mobile': mobile, 'category': categoty})
    quzhou.store.insert({'name': name, 'mobile': mobile, 'category': categoty})


def url_with_page(url, pages):
    for i in range(1, pages + 1):
        yield url + '/p' + str(i)

urls = url_with_page('http://www.dianping.com/search/category/106/45', 18)


def get_mobile(href):
    req = Request('http://www.dianping.com' + href, data=None, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'})
    with urlopen(req) as f:
        data = f.read()
    soup = BeautifulSoup(data)
    mobiles = soup.find_all('span', attrs={'class': 'item', 'itemprop': 'tel'})
    return [x.text for x in mobiles]


def scrapy():
    for url in urls:
        req = Request(url, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'})

        with urllib.request.urlopen(req) as f:
            html = f.read()
        soup = BeautifulSoup(html)

        div = soup.find('div', id='shop-all-list')
        ul = div.ul
        lis = ul.find_all('li')
        for li in lis:
            a_s = li.find_all('a')
            href = a_s[0]['href']
            # time.sleep(5)
            mobiles = get_mobile(href)
            insert_into_mongodb('quzhou', a_s[1]['title'], li.find('span', attrs={'class': 'tag'}).text, mobiles)
        # time.sleep(5)


if __name__ == '__main__':
    scrapy()
