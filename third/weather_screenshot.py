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


def weather_screen_shot(city):
    # 设置浏览器
    options = Options()
    options.add_argument('--no-sandbox')
    # 无头参数
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # 创建浏览器选项对象
    # 启动浏览器
    driver = Chrome(options=options)
    driver.maximize_window()
    try:
        # 访问页面
        url = f'https://www.tianqi.com/{city}'
        driver.get(url)
        time.sleep(5)
        # 设置截屏整个网页的宽度以及高度
        scroll_width = 1920
        scroll_height = 1080
        driver.set_window_size(width=scroll_width, height=scroll_height)
        # 往下滚动
        # driver.execute_script("window.scrollTo(0, 125);")
        # 保存图片
        img_name = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        img_url = "%s.png" % os.path.join(img_tmp_path, img_name)
        driver.get_screenshot_as_file(img_url)
        # 关闭浏览器
        # driver.close()
        # driver.quit()
        return img_url
    except Exception as e:
        print(e)


def cdrop(img_url):
    img = Image.open(img_url)
    width, height = img.size
    # 前两个坐标点是左上角坐标
    # 后两个坐标点是右下角坐标
    # 左、上、右、下
    box = (270, 310, 910, 570)
    region = img.crop(box)
    region.save(f'{img_tmp_path}/crop.png')


if __name__ == '__main__':
    cdrop('E:\GitRepo\wechat-girlfriend-push\img\\tmp\\2023-02-25-16-42-44.png')
