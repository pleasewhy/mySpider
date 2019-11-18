# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer,DateTime,ForeignKey,Text


engine = create_engine('mysql+pymysql://root:123456@localhost:3306/wangyiyun?charset=utf8mb4')
Base = declarative_base()

class Song(Base):

    __tablename__ = 'song'

    song_id = Column(Integer, primary_key=True)  # 网易云的歌曲id
    song_name = Column(String(128)) # 歌曲名称
    singer_id = Column(Integer)  # 歌手id
    singer_name = Column(String(32))  # 歌手
    album_name =  Column(String(32))  # 所属专辑
    total = Column(Integer, index=True) # 该歌曲评论总数
    crawl_time = Column(DateTime)  # 爬取时间
    time_modified = Column(DateTime)  # 修改时间


    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)


class Comment(Base):
    """docstring for comment"""
    __tablename__  = 'comment'

    id = Column(Integer, primary_key=True)  # 评论id自动增长
    song_id = Column(Integer) # 该评论所属歌曲的id
    nickname = Column(String(32))  # 评论人
    likedCount = Column(Integer)  # 点赞数量
    content = Column(Text)  # 评论内容  
    comment_time = Column(DateTime)  # 评论时间
    time_create = Column(DateTime)  # 创建时间
    time_modified = Column(DateTime)  # 最后一次修改时间

    
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)


class Singer(Base):
    """docstring for siger"""
    __tablename__ = 'singer'

    singer_id = Column(Integer, primary_key=True)
    name = Column(String(128))


    def __repr__(self):
        return '%s(r%)' % (self.__class__.__name__, self.username)

# Base.metadata.create_all(engine)  # 创建表
# Singer.metadata.create_all(engine)  # 创建单个表
Session = sessionmaker(bind=engine)
session = Session()
session.rollback()