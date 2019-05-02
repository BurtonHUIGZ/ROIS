# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from .settings import IMAGES_STORE
import requests
class RoisPipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        header = {
            'USER-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Cookie': 'b963ef2d97e050aaf90fd5fab8e78633',
            # 需要查看图片的cookie信息，否则下载的图片无法查看
        }
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images')
        item['item_paths'] = image_paths

        images = []
        dir_path = '{}'.format(IMAGES_STORE)
        for jpg_url, name, num in zip(item['image_urls'], item['alt'], range(0, 100)):
            file_name = name + str(num)
            file_path = '{}//{}'.format(dir_path, file_name)
            images.append(file_path)
            if os.path.exists(file_path) or os.path.exists(file_name):
                continue

            with open('{}//{}.jpg'.format(dir_path, file_name), 'wb') as f:
                req = requests.get(jpg_url, headers=header)
                f.write(req.content)

        return item
