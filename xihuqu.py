import urllib.request
from urllib.request import Request, urlopen
import pymongo
from bs4 import BeautifulSoup


xihuqu = pymongo.MongoClient('127.0.0.1:27017').xihuqu


def insert_into_mongodb(name, categoty, mobile):
    xihuqu.store.insert({'name': name, 'mobile': mobile, 'category': categoty})


def url_with_page(url, pages):
    for i in range(1, pages + 1):
        yield url + 'p' + str(i)

urls = url_with_page('http://www.dianping.com/search/category/3/45/r62', 41)
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'}


def get_mobile(href):
    req = Request('http://www.dianping.com' + href, data=None, headers=header)
    with urlopen(req) as f:
        data = f.read()
    soup = BeautifulSoup(data)
    mobiles = soup.find_all('span', attrs={'class': 'item', 'itemprop': 'tel'})
    return [x.text for x in mobiles]


def scrapy():
    for url in urls:
        req = Request(url, data=None, headers=header)

        with urllib.request.urlopen(req) as f:
            html = f.read()
        soup = BeautifulSoup(html)

        div = soup.find('div', id='shop-all-list')
        ul = div.ul
        lis = ul.find_all('li')
        for li in lis:
            a_s = li.find_all('a')
            href = a_s[0]['href']
            mobiles = get_mobile(href)
            insert_into_mongodb('xihuqu', a_s[1]['title'], li.find('span', attrs={'class': 'tag'}).text, mobiles)


if __name__ == '__main__':
    scrapy()
