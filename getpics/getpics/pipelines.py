# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import json
import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.conf import settings
# import pymongo
from scrapy import log
import hashlib
from getpics.sucess import sucess



class GetpicsPipeline(object):
	pass


class JsonWritePipeline(object):

	def __init__(self):
		self.file = open('item.json', 'wb')
	def process_item(self, item, spider):

		# for title in item['title']:
			# print title
			# item['title'] = str(title).decode('ascii').encode('utf-8')
		line = json.dumps(dict(item), ensure_ascii=False).encode('utf-8') + '\n'
		self.file.write(line)
		# log.msg("write to json file")
		return item

class CreatFloderPipeline(object):

	def process_item(self, item, spider):
		for title in item['title']:
			img_path = "../pictures/" + title.encode('utf-8')
			if not os.path.exists(img_path):
				# print '-'*100	
				os.mkdir(img_path)
				log.msg("sucess creat folder " + img_path)

		return item

class MongoWritePipeline(object):
	def __init__(self):
		host = settings['MONGODB_HOST']
		port = settings['MONGODB_PORT']
		dbName = settings['MONGODB_DBNAME']
		client = pymongo.MongoClient(host=host, port=port)
		tdb = client[dbName]
		self.post = tdb[settings['MONGODB_DOCNAME']]
	def process_item(self, item, spider):
		postInfo = dict(item)
		self.post.insert(postInfo)
		return item	
		
class MyImagesPipeline(ImagesPipeline):
	def file_path(self, request, response=None, info=None):
		url = request.url
		image_guid = hashlib.sha1(url).hexdigest()
		return 'full/%s/%s.jpg' % (image_guid[:-2], image_guid)

	def thumb_path(self, request,thumb_id, response=None, info=None):
		url = request.url
		thumb_guid = hashlib.sha1(url).hexdigest()
		return 'thumb/%s/%s.jpg' % (thumb_guid[:-2], thumb_guid)

	# def get_images(self, response, request, info):
	# 	pass

	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			yield scrapy.Request(image_url)

	def item_completed(self, results, item, info):
		image_paths = [x['path'] for ok, x in results if ok]
		item['image_paths'] = image_paths
		sucess()
		return item
