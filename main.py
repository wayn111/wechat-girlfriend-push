import datetime
import json
import os
import random
import time

import jwt
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from third.image_util import ImageUtil
from third.logger import logger
from third.myemail import Email
from third.qiyeweixin import QiWeixin
from third.weather_screenshot import cdrop, screen_shot

# 自动搜索.env文件
load_dotenv(verbose=True)
img_tmp_path = os.getenv('img_tmp_path')
together_day_str = os.getenv('together_day')
wecom_cid = os.getenv('wecom_cid')
wecom_aid = os.getenv('wecom_aid')
wecom_secret = os.getenv('wecom_secret')

chp_color_arr = [
    'pink', 'lightpink', 'deeppink', 'aqua', 'chocolate',
    'crimson', 'darkseagreen', 'violet', 'plum', 'greenyellow'
]

def check_json_format(raw_msg):
    """
    用于判断一个字符串是否符合Json格式
    :param self:
    :return:
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg)
        except ValueError:
            return False
        return True
    else:
        return False


def decode_jwt(token):
    result = jwt.decode(token, algorithms=["HS256"], options={
        'verify_exp': False, "verify_signature": False})
    return result['username']


def get_weekdays():
    """
    :return: week_name_cn
    """
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    local_time = time.localtime(time.time())  # 获取当前时间的时间元组
    # time.struct_time(tm_year=2022, tm_mon=4, tm_mday=9, tm_hour=13, tm_min=48, tm_sec=23, tm_wday=5, tm_yday=99, tm_isdst=0)

    week_index = local_time.tm_wday  # 获取时间元组内的tm_wday值
    week = week_list[week_index]
    return week


def weather_v2(city_weather='东莞市凤岗镇天气'):
    try:
        now_day = time.localtime(time.time())  # 得到结构化时间格式
        now = time.strftime("%Y-%m-%d", now_day)
        week = get_weekdays()
        img_url = screen_shot(city_weather)
        cdrop(img_url)
        token = QiWeixin.get_token(wecom_cid, wecom_secret)
        result = ImageUtil.upload_image(image_path=f'{img_tmp_path}/crop.png',
                                        url=f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={token}&type=image')
        tmp_media_id = result['media_id']
        chp_text = QiWeixin.get_chp_text()

        together_day = datetime.datetime.strptime(together_day_str, '%Y-%m-%d')  # 注意str的格式要与'%Y-%m-%d'相匹配。
        diff_day_num = (datetime.datetime.now().__sub__(together_day)).days

        wallpaper_url = QiWeixin.get_bing_wallpaper()

        img_local_path = ImageUtil.download_image(img_tmp_path, wallpaper_url)
        result = ImageUtil.upload_image(image_path=img_local_path,
                                        url=f'https://qyapi.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}')
        img_url = result['url']

        chp_text_color = chp_color_arr[random.randint(1, 10)]
        mpnews = {
            "title": "柯宝的专属通知😘",
            "thumb_media_id": f'{tmp_media_id}',
            "author": "waynaqua",
            "content": f"""
            <div style="color:green;">{now} {week}</div>
            <div>今天是我们在一起的第<span style="color:lightcoral;">{diff_day_num}</span>天</div>
            <img src="{img_url}">
            <br />
            <div style="color:{chp_text_color};">{chp_text}</div> 
            """,
            "digest": "东莞市凤岗镇天气"
        }
        QiWeixin.send_mpnews(mpnews, wecom_cid, wecom_secret, wecom_aid)
    except Exception as e:
        logger.exception(e)
        Email.send_error_email('python执行异常：{}'.format(e))
    finally:
        ImageUtil.del_file(img_tmp_path)

interval_task = {
    # 配置存储器
    "jobstores": {
        # 使用内存进行存储
        'default': MemoryJobStore()
    },
    # 配置执行器
    "executors": {
        # 使用进程池进行调度，最大进程数是10个
        'default': ProcessPoolExecutor(1)
    },
    # 创建job时的默认参数
    "job_defaults": {
        'coalesce': False,  # 是否合并执行
        'max_instances': 3,  # 最大实例数
    }
}

apsched = AsyncIOScheduler(**interval_task, timezone="Asia/Shanghai")

apsched.add_job(weather_v2, 'cron', hour='7,11,17', minute=45, second=30, args=['东莞市凤岗镇天气'])

if __name__ == '__main__':
    apsched.start()
