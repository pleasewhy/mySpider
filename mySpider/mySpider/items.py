# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WangYiYunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    song_name = scrapy.Field() # 歌曲名称	
    song_id = scrapy.Field()  # 网易云的歌曲id
    singer_name = scrapy.Field()  # 歌手
    singer_id = scrapy.Field()  # 网易云的歌手id
    album_name = scrapy.Field()  # 所属专辑
    hotComments = scrapy.Field()  # 热评列表，热评包含nickname，starCount，content
    total = scrapy.Field()	# 该歌曲评论总数
    fan_num = scrapy.Field()  # 歌手的粉丝总数
    crawl_time = scrapy.Field()  # 爬取时间