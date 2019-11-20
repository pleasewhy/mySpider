# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from mySpider.WangYiYunTable import *
# 将爬取到的数据存储到数据库
# 注意：添加失败需要回滚不然会一直添加该错误信息
class MyspiderPipeline(object):
    def process_item(self, item, spider):
        if not session.query(Singer).filter_by(singer_id=item["singer_id"]).first():
            try:
                session.add(Singer(singer_id=item['singer_id'], name=item['singer_name']))
                session.commit()
            except:
                session.rollback()

        if not session.query(Song).filter_by(song_id=item["song_id"]).first():
            try:
                session.add(Song(
                            song_id=item["song_id"],
                            song_name=item["song_name"],
                            singer_id=item["singer_id"],
                            singer_name=item["singer_name"],
                            album_name=item["album_name"],
                            total=item['total'],
                            crawl_time=item['crawl_time'],
                            time_modified=item['crawl_time'])
                        )
                session.commit()
            except:
                session.rollback()

        try:
            for comment in item["hotComments"]:
                session.add(Comment(
                                    song_id = item["song_id"],
                                    nickname = comment["nickname"],
                                    likedCount = comment["likedCount"],
                                    content = comment["content"],
                                    comment_time = comment['time'],   
                                    time_create = item['crawl_time'],
                                    time_modified = item['crawl_time']
                                    )
                            )
                session.commit()
        except:
            session.rollback()

        return item