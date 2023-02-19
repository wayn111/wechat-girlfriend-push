import json

import requests
import random

class QiWeixin(object):

    @classmethod
    def send_qiye(cls, messgae, wecom_cid, wecom_aid, wecom_secret, wecom_touid='@all'):
        token = cls.get_token(wecom_cid, wecom_secret)
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?debug=1&access_token={}'.format(
            token)
        json_data = {
            'touser': wecom_touid,
            'agentid': wecom_aid,
            'msgtype': 'textcard',
            'textcard': messgae,
            'duplicate_check_interval': 600,
        }
        resp = requests.post(url, json=json_data)
        content = resp.content.decode('utf-8')
        content = json.loads(content)
        if content['errcode'] != 0:
            raise Exception(content)
        return True

    @classmethod
    def get_userid(cls, wecom_cid, wecom_secret, mobile):
        token = cls.get_token(wecom_cid, wecom_secret)
        url = 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserid?debug=1&access_token={}'.format(
            token)
        json_data = {
            'mobile': mobile,
        }
        resp = requests.post(url, json=json_data)
        content = resp.content.decode('utf-8')
        return json.loads(content)

    @classmethod
    def get_invite_code(cls, wecom_cid, wecom_secret, mobile):
        token = cls.get_token(wecom_cid, wecom_secret)
        url = 'https://qyapi.weixin.qq.com/cgi-bin/corp/get_join_qrcode?access_token={}'.format(
            token)
        json_data = {
            'mobile': mobile,
        }
        resp = requests.post(url, json=json_data)
        content = resp.content.decode('utf-8')
        return json.loads(content)

    @classmethod
    def send_mpnews(cls, messgae, wecom_cid, wecom_secret, wecom_aid, wecom_touid='@all'):
        token = cls.get_token(wecom_cid, wecom_secret)
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?&access_token={}'.format(
            token)
        json_data = {
            'touser': wecom_touid,
            'agentid': wecom_aid,
            'msgtype': 'mpnews',
            'mpnews': {
                "articles": [messgae]
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 600
        }
        resp = requests.post(url, json=json_data)
        content = resp.content.decode('utf-8')
        content = json.loads(content)
        if content['errcode'] != 0:
            raise Exception(content)
        return True

    @classmethod
    def get_token(cls, wecom_cid, wecom_address_secret):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(
            wecom_cid, wecom_address_secret)
        resp = requests.get(url)
        content = resp.content.decode('utf-8')
        content = json.loads(content)
        if content['errcode'] != 0:
            raise Exception(content)
        return content['access_token']

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

