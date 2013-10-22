#!/usr/bin/env python

######################################################
#
# eBay Collection Creator
# Usage: `python collect.py -c <collection_id>`
# Written by Benjamin Gleitzman (gleitz@mit.edu)
#
######################################################

import argparse
import cookielib
import json
import requests
import StringIO
import urllib

from pyquery import PyQuery as pq

ADD_ITEM_TO_COLLECTION_URL = 'http://svcs.ebay.com/buying/collections/v1/collection/{0}/item'

def _fetch_cookies():
    cookies = cookielib.MozillaCookieJar('cookies.txt')
    s = StringIO.StringIO()
    s.write("""\
# Netscape HTTP Cookie File
# http://www.netscape.com/newsref/std/cookie_spec.html
# This is a generated file!  Do not edit.
""")
    with open('cookies.txt') as f:
        for line in f:
            if line.startswith('.ebay.com'):
                s.write(line)
        s.seek(0)
        print s.getvalue()
        cookies._really_load(s, '', True, True)
        return cookies


def add_to_collection(item_id, collectionid):
    data = {'method': 'post',
            'addItemsRequest': json.dumps([{"itemId" : item_id,
                                            "variationId": 0,
                                            "note": ""}])}
    url = '{0}?{1}'.format(ADD_ITEM_TO_COLLECTION_URL.format(collectionid),
                         urllib.urlencode(data))
    r = requests.get(url,
                     cookies = _fetch_cookies())
    print r.json()

def find_item(keyword):
    url = 'http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=JasonKot-143b-4404-8b22-382716c52aa8&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords={0}'.format(keyword)
    print url
    r = requests.get(url)
    try:
        item_id = str(r.json()['findItemsByKeywordsResponse'][0]
                     ['searchResult'][0]['item'][0]['itemId'][0])
        return item_id
    except Exception, e:
        return None

def fetch_broke_items(collection_id):
    item_ids = []
    url = 'http://www.thisiswhyimbroke.com/popular/?infinity=scrolling&action=infinite_scroll&page={0}&order=DESC'
    for x in range(15):
        html = requests.get(url.format(x)).json()['html']
        html = pq(html)
        for title in html('.title'):
            try:
                title = title.find('a').text
            except Exception, e:
                continue
            print title
            item_id = find_item(title.encode('utf-8'))
            if item_id:
                item_ids.append(item_id)
                print 'http://www.ebay.com/itm/' + item_id


    item_ids.reverse()
    for item_id in item_ids:
        add_to_collection(item_id, collection_id)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='eBay Collection Creator')
    parser.add_argument('-c', '--collection-id',
                        help='the id of the collection', type=str, required=True)
    args = vars(parser.parse_args())
    fetch_broke_items(args['collection_id'])
