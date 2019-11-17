import scrapy
from mySpider.items import WangYiYunItem
import time
from datetime import datetime
import json
import random

class WangYiYunSpider(scrapy.Spider):
    name = "wangyiyun"
    base_url = "https://music.163.com"
    start_urls = ["https://music.163.com/discover/artist/cat?id=1001"]
    now_id = None # 用于爬取
    comment_key = ['likedCount','content','user','time']  # nickname是包含在user中


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.parseDiscoverPage)
            

    def parseDiscoverPage(self, response):
        print()
        # 得到歌手列表元素（前100）
        all_singer_list = response.xpath('//ul[@class="m-cvrlst m-cvrlst-5 f-cb"]/li')
        # 得到歌手的用户页面（得到其粉丝数量）和歌手页面
        for index, singer in enumerate(all_singer_list):
            if index < 10: 
                url = self.base_url+singer.xpath('.//p/a/@href').get().strip()
            else:
                url = self.base_url+singer.xpath('.//a/@href').get().strip()
            yield scrapy.Request(url=url, callback=self.parseSingerPage)


    def parseSingerPage(self, response):
        hot_50_songs_list = response.xpath('//ul[@class="f-hide"]/li/a/@href').getall()
        for url in map(lambda x:self.base_url+x.strip(), hot_50_songs_list):
            yield scrapy.Request(url=url, callback=self.parseSongPage)

    def parseSongPage(self, response):
        """<meta property="og:music:play" content="https://music.163.com/song?id=1346104327" />
            <meta property="og:music:artist" content="隔壁老樊" />
            <meta property="og:music:album" content="我曾"/>
            <meta property="music:album" content="https://music.163.com/album?id=75019098"/>
            <meta property="music:duration" content="269"/>
            <meta property="music:musician" content="https://music.163.com/artist?id=12429072"/>
            <meta property="og:title" content="多想在平庸的生活拥抱你" />"""
        song_name = response.xpath('//meta[@property="og:title"]/@content').get()
        song_id = response.xpath('//meta[@property="og:music:play"]/@content').get().split("id=")[-1]
        singer_name = response.xpath('//meta[@property="og:music:artist"]/@content').get()
        singer_id = response.xpath('//meta[@property="music:musician"]/@content').get().split("id=")[-1]
        album_name = response.xpath('//meta[@property="og:music:album"]/@content').get()
        crawl_time = datetime.now().__str__().split('.')[0]
        # print(song_name,"\n\n")
        wyy_item = WangYiYunItem(
            song_id=song_id,
            singer_name=singer_name,
            singer_id=singer_id,
            album_name=album_name,
            crawl_time=crawl_time,
            song_name=song_name
            )
        return scrapy.Request(url="https://music.163.com/api/v1/resource/comments/R_SO_4_"+str(song_id),
                        callback=self.parseHotComment,cb_kwargs=dict(wyy_item=wyy_item))


    def parseHotComment(self,response,wyy_item):
        response_dict = json.loads(str(response.body,encoding = "utf-8"))
        total = response_dict['total']
        hotComments = response_dict['hotComments']
        wyy_item['hotComments'] = self.getCommentInfo(hotComments)
        wyy_item['total'] = total
        return wyy_item


    # 得到评论中的nickname,content,likedCount,time
    # 并将time(时间戳)转化为datetime类型
    def getCommentInfo(self,hotComments):
        hotComments = list(map(lambda x:{key:x[key] for key in self.comment_key}, hotComments))
        for comment in hotComments:
            comment['nickname'] = comment['user']['nickname']
            time_local = time.localtime(comment['time']/1000) # 将毫秒时间戳转化为秒时间戳
            comment['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            comment.pop('user')
        #转换成新的时间格式(2019-11-13 15:48:20)
        return list(hotComments)