# -*- coding: utf-8 -*-

#   {"c":{"date":"2016-3-23","items":[{"area":"可售房屋面积(M2):9122839.0400","count":"可售房屋套数:96611","detail":
# {"carA":"面积(M2):2903892.2300","carC":"车位个数:35585","comA":"面积(M2):974084.8800","comC":"商业单元:7387",
# "houA":"面积(M2):4299898.5900","houC":"  其中    住宅套数:32055","offA":"面积(M2):687784.6000","offC":"办公单元:17733"},
# "title":"可售期房统计"},{"area":"批准预售面积(M2):174154.9200","count":"批准预售许可证:4","detail":{"carA":"面积(M2):21193.9800",
# "carC":"车位个数:470","comA":"面积(M2):37531.5800","comC":"商业单元:1","houA":"面积(M2):52316.7400",
# "houC":"  其中   住宅套数:675","offA":"面积(M2):29219.9100","offC":"办公单元:325"},"title":"2016年2月预售许可"},
# {"area":"网上认购面积(M2):13242.4600","count":"网上认购套数:103","detail":{"carA":"面积(M2):0.0000","carC":"车位个数:0",
# "comA":"面积(M2):309.4900","comC":"商业单元:3","houA":"面积(M2):12404.9700","houC":"  其中   住宅套数:93",
# "offA":"面积(M2):528.0000","offC":"办公单元:7"},"title":"期房网上认购"},{"area":"网上签约面积(M2):35420.2900",
# "count":"网上签约套数:427","detail":{"carA":"面积(M2):788.8800","carC":"车位个数:19","comA":"面积(M2):2442.6400",
# "comC":"商业单元:24","houA":"面积(M2):24846.2600","houC":" 其中    住宅套数:264","offA":"面积(M2):7201.9000","offC":"办公单元:117"},
# "title":"期房网上签约"},{"area":"未签约面积(M2):11507656.5500","count":"未签约套数:114627","detail":{"carA":"面积(M2):2005457.1700",
# "carC":"车位个数:47336","comA":"面积(M2):1659220.1400","comC":"商业单元:6522","houA":"面积(M2):4593817.8700",
# "houC":"    其中  住宅套数:35999","offA":"面积(M2):1841666.5400","offC":"办公单元:14727"},"title":"未签约现房统计"},
# {"area":"初始登记面积(M2):214491171.5000","count":"现房项目个数:23404","detail":{"carA":"面积(M2):14302610.7500",
# "carC":"车位个数:355618","comA":"面积(M2):15148618.6400","comC":"商业单元:68072","houA":"面积(M2):93898647.1400",
# "houC":"  其中   住宅套数:758179","offA":"面积(M2):12703609.6800","offC":"办公单元:66441"},"title":"现房项目情况"},
# {"area":"网上认购面积(M2):13933.4700","count":"网上认购套数:103","detail":{"carA":"面积(M2):0.0000","carC":"车位个数:0",
# "comA":"面积(M2):0.0000","comC":"商业单元:0","houA":"面积(M2):13258.0900","houC":"  其中   住宅套数:96","offA":"面积(M2):634.8300",
# "offC":"办公单元:6"},"title":"现房网上认购"},{"area":"网上签约面积(M2):18664.9500","count":"网上签约套数:191",
# "detail":{"carA":"面积(M2):2535.9700","carC":"车位个数:71","comA":"面积(M2):1127.4300","comC":"商业单元:9",
# "houA":"面积(M2):9677.1400","houC":"  其中   住宅套数:63","offA":"面积(M2):3877.0000","offC":"办公单元:42"},"title":"现房网上签约"}],
# "month":"2016 年2月","title":"现房网上签约"},"s":{"items":[{"area":"可售房源面积(m2):3934386.5160","area2":"可售住宅面积(m2):3536093.9760",
# "cou":"可售房源套数:39098","cou2":"可售住宅套数:36656","tit":"可售房源统计"},{"area":"新发布房源面积(m2):137834.7700",
# "area2":"新发布住宅面积(m2):129679.6400","cou":"新发布房源套数:1520","cou2":"新发布住宅套数:1395","tit":"2016-3-23新发布房源"},
# {"area":"网上签约面积(m2):1520722.3100","area2":"住宅签约面积(m2):1378375.7900","cou":"网上签约套数:16583","cou2":"住宅签约套数:15149",
# "tit":"2016年2月存量房网上签约"},{"area":"网上签约面积(m2):142130.9700","area2":"住宅签约面积(m2):133057.8000","cou":"网上签约套数:1583",
# "cou2":"住宅签约套数:1441","tit":"2016-3-23存量房网上签约"}]},"t":"1458662400000"}

import json
import leancloud
import re
import sys
import time
import urllib2
from leancloud import LeanCloudError
from leancloud import Object


class HouseParser:
    def __init__(self):
        self.Url = "http://www.bjjs.gov.cn/tabid/2167/default.aspx?COLLCC=2389390305&COLLCC=2937872865&"
        self.jsonBean = {}
        self.commercial_title = ['可售期房统计', '预售许可', '期房网上认购', '期房网上签约', '未签约现房统计', '现房项目情况',
                                 '现房网上认购', '现房网上签约']
        self.stock_title = ['可售房源统计', '新发布房源', '存量房网上签约', '存量房网上签约']

    def print_str(self, s):
        type = sys.getfilesystemencoding()
        print s.decode('UTF-8').encode(type)

    def get(self, url):
        request = urllib2.Request(url);
        try:
            response = urllib2.urlopen(request)
            read = response.read()
            return read
        except urllib2.HTTPError, e:
            print'Get content failed:' + e.code
            return

    def read_content(self):
        print'Get content from Net.'
        # with open("content.txt", 'r') as f:
        #     content = f.read().decode('utf-8')
        content = self.get(self.Url).decode('utf-8')
        if content:
            # remove &nbsp
            pattern = re.compile(r'&nbsp;')
            txt = pattern.sub(" ", content)
            print'Get content success.'
            return txt
        else:
            return

    def parse(self):
        content = self.read_content()
        if content:
            print'Start to parse content'
            commercial_bean = {}
            pattern = re.compile(r'<tr[^<>]+><td[^<>]+><span[^<>]+>([^<>]+)</span>')
            date = pattern.search(content)
            if date:
                commercial_bean['date'] = date.group(1)
                self.jsonBean['t'] = time.mktime(time.strptime(date.group(1), '%Y-%m-%d')) * 1000

            commercial = re.findall(
                    r'<tr[^<>]+><td[^<>]+>([^<>(：]+).*</td>\s+<td[^<>]+><span [^<>]+>([^<>]+).*</span></td></tr>'.decode(
                            "utf8"),
                    content)
            if commercial:
                items_queue = []
                for i in range(8):
                    item = {}
                    detail = {}
                    item['count'] = commercial[i * 10][0] + ":" + commercial[i * 10][1]
                    item['title'] = self.commercial_title[i]
                    item['area'] = commercial[i * 10 + 1][0] + ":" + commercial[i * 10 + 1][1]
                    detail['houC'] = commercial[i * 10 + 2][0] + ":" + commercial[i * 10 + 2][1]
                    detail['houA'] = commercial[i * 10 + 3][0] + ":" + commercial[i * 10 + 3][1]
                    detail['comC'] = commercial[i * 10 + 4][0] + ":" + commercial[i * 10 + 4][1]
                    detail['comA'] = commercial[i * 10 + 5][0] + ":" + commercial[i * 10 + 5][1]
                    detail['offC'] = commercial[i * 10 + 6][0] + ":" + commercial[i * 10 + 6][1]
                    detail['offA'] = commercial[i * 10 + 7][0] + ":" + commercial[i * 10 + 7][1]
                    detail['carC'] = commercial[i * 10 + 8][0] + ":" + commercial[i * 10 + 8][1]
                    detail['carA'] = commercial[i * 10 + 9][0] + ":" + commercial[i * 10 + 9][1]
                    item['detail'] = detail
                    items_queue.append(item)
                commercial_bean['items'] = items_queue
                self.jsonBean['c'] = commercial_bean
            stock = re.findall(
                    r'<tr[^<>]+>\s*<td[^<>]+>([^<>(：]+).*\s+</td>\s+<td[^<>]+>\s+<span[^<>]+>([^<>]+)</span>\s+'.decode(
                            "utf8"),
                    content)
            if stock:
                stock_bean = {}
                item_queue = []
                for i in range(4):
                    item = {}
                    item['tit'] = self.stock_title[i]
                    item['cou'] = stock[i * 4][0].strip() + ":" + stock[i * 4][1].strip()
                    item['area'] = stock[i * 4 + 1][0].strip() + ":" + stock[i * 4 + 1][1].strip()
                    item['cou2'] = stock[i * 4 + 2][0].strip() + ":" + stock[i * 4 + 2][1].strip()
                    item['area2'] = stock[i * 4 + 3][0].strip() + ":" + stock[i * 4 + 3][1].strip()
                    item_queue.append(item)
                stock_bean['items'] = item_queue
                self.jsonBean['s'] = stock_bean
            jsonstr = json.dumps(self.jsonBean).decode('unicode_escape')
            print 'Parse complete.'
            self.update_data(jsonstr)
            # with open("result.txt", 'w') as f:
            #     f.write(jsonstr.encode('utf8'))

    def update_data(self, data):
        print ('Update data to server')
        JSON_TNAME = "JSON_TNAME";
        JSON_DATE = "JSON_DATE"
        JSON_TIME = "JSON_TIME"
        JSON_CONTENT = "JSON_CONTENT"
        leancloud.init('yourid', 'yourkey')
        BeanObj = Object.extend(JSON_TNAME)
        leanObj = BeanObj()

        leanObj.set('JSON_DATE', self.jsonBean['c']['date'])
        leanObj.set('JSON_TIME', int(self.jsonBean['t']))
        leanObj.set('JSON_CONTENT', data)
        try:
            leanObj.save()
            print 'Update success.'
        except LeanCloudError, e:
            print 'update failed' + e


if __name__ == '__main__':
    print'Start to run.'
    parser = HouseParser()
    parser.parse()
