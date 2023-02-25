import json

import requests
import random
from lxml import etree


class Service(object):

    @classmethod
    def get_chp_text(cls):
        url = 'https://api.shadiao.pro/chp'
        res = requests.get(url)
        return res.json()['data']['text']

    @classmethod
    def get_bing_wallpaper(cls):
        url = f'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=7'
        res = requests.get(url)
        n = random.randint(0, 4)
        return "https://cn.bing.com" + res.json()['images'][n]['url']

    @classmethod
    def xing_zuo(cls, girl_born_date):
        constellation_date_range = [
            ["0321", "0419"], ["0420", "0520"], ["0521", "0621"], ["0622", "0722"],
            ["0723", "0822"], ["0823", "0922"], ["0923", "1023"], ["1024", "1122"],
            ["1123", "1221"], ["1222", "1231", "0101", "0119"], ["0120", "0218"], ["0219", "0320"]
        ]
        constellation_cn = ['白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手', '摩羯', '水瓶',
                            '双鱼']
        constellation_en = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius',
                            'capricorn', 'aquarius', 'pisces']
        xing_zuo_list = []
        for idx, val in enumerate(constellation_date_range):
            if len(val) == 2:
                begin = int(val[0])
                end = int(val[1])
                if begin < girl_born_date < end:
                    xing_zuo_list = [constellation_cn[idx], constellation_en[idx]]
            if len(val) == 4:
                begin1 = int(val[0])
                end1 = int(val[1])
                begin2 = int(val[2])
                end2 = int(val[3])
                if begin1 < girl_born_date < end1 or begin2 < girl_born_date < end2:
                    xing_zuo_list = [constellation_cn[idx], constellation_en[idx]]
        xing_zuo_cn = xing_zuo_list[0]
        xing_zuo_en = xing_zuo_list[1]
        resp = requests.get(
            url=f'https://www.xzw.com/fortune/{xing_zuo_en}',)
        tree = etree.HTML(resp.text)
        content = tree.xpath('//*[@id="view"]/div[2]/div[3]/div[2]/p[1]/span')
        return [xing_zuo_cn, content[0].text]
