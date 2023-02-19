import json
import os.path
import time

from PIL import Image
from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

tianqi_arr = [
    '⛅', '☀️', '🌦️', '❄️', '⛈️', '💧'
]

# 自动搜索.env文件
load_dotenv(verbose=True)
img_tmp_path = os.getenv('img_tmp_path')


def screen_shot(city):
    # 设置浏览器
    options = Options()
    options.add_argument('--no-sandbox')
    # 无头参数
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # 替换User-Agent
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50')
    # 创建浏览器选项对象
    # 启动浏览器
    driver = Chrome(options=options)
    driver.maximize_window()
    try:
        # 访问页面
        url = f'https://so.toutiao.com/search?wid_ct=1676801414471&dvpf=pc&source=input&keyword={city}&page_num=0&pd=synthesis'
        driver.get(url)
        driver.add_cookie({'name': 'ttwid',
                           'value': '1%7Cf-KdTK9I1GyXCCNp5FxDYQj2uCP3ozk1E7GsMoDrENw%7C1674919873%7Ce0678f6f1a24b5fb4db4dc4a475971da28ec73eae0a6271080a8031a20be93c5'})
        time.sleep(3)
        # 设置截屏整个网页的宽度以及高度
        scroll_width = 1920
        scroll_height = 1080
        driver.set_window_size(width=scroll_width, height=scroll_height)
        # 往下滚动
        # driver.execute_script("window.scrollTo(0, 125);")
        # 保存图片
        img_name = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        imgUrl = "%s.png" % os.path.join(img_tmp_path, img_name)
        driver.get_screenshot_as_file(imgUrl)
        # 关闭浏览器
        driver.close()
        driver.quit()
        return imgUrl
    except Exception as e:
        print(e)


def cdrop(imgUrl):
    img = Image.open(imgUrl)
    width, height = img.size
    # 前两个坐标点是左上角坐标
    # 后两个坐标点是右下角坐标
    # 左、上、右、下
    box = (145, 165, 765, 680)
    region = img.crop(box)
    region.save(f'{img_tmp_path}/crop.png')
