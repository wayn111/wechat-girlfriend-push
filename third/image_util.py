import json
import os
import uuid

import requests
from PIL import Image
from PIL import ImageFile


class ImageUtil(object):

    # 输入pip install requests_toolbelt 安装依赖库
    @classmethod
    def upload_image(cls, image_path, name="media", url=""):
        files = {name: (open(image_path, 'rb'))}  # 需要替换具体的path
        headers = {}
        response = requests.request("POST", url, headers=headers, files=files)
        return json.loads(response.content)

    # 压缩图片文件
    @classmethod
    def compress_image(cls, outfile, mb=10, quality=80, k=0.7):  # 通常你只需要修改mb大小
        """不改变图片尺寸压缩到指定大小
        :param outfile: 压缩文件保存地址
        :param mb: 压缩目标，KB
        :param k: 每次调整的压缩比率
        :param quality: 初始压缩比率
        :return: 压缩文件地址，压缩文件大小
        """

        o_size = os.path.getsize(outfile) // 1024  # 函数返回为字节，除1024转为kb（1kb = 1024 bit）
        print('before_size:{} after_size:{}'.format(o_size, mb))
        if o_size <= mb:
            return outfile

        ImageFile.LOAD_TRUNCATED_IMAGES = True  # 防止图像被截断而报错
        while o_size > mb:
            try:
                with Image.open(outfile) as im:
                    x, y = im.size
                    im.thumbnail((int(x * k), int(y * k)))  # 最后一个参数设置可以提高图片转换后的质量
                    im.save(outfile, quality=quality)  # quality为保存的质量，从1（最差）到95（最好），此时为85
                    o_size = os.path.getsize(outfile) // 1024
                    print(o_size)
            except Exception as e:
                print(e)
        return outfile

    @classmethod
    def download_image(cls, img_tmp_path, img_url):
        response = requests.get(img_url, stream=True)
        img_local_path = img_tmp_path + '/' + str(uuid.uuid1()).replace('-', '') + '.png'
        with open(img_local_path, 'wb') as logFile:
            for chunk in response:
                logFile.write(chunk)
            logFile.close()
            print("Download done!")
        return img_local_path

    @classmethod
    def del_file(cls, path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):  # 如果是文件夹那么递归调用一下
                cls.del_file(c_path)
            else:  # 如果是一个文件那么直接删除
                os.remove(c_path)
        print('文件已经清空完成')
