# -*- coding: utf-8 -*-

import CommonFunction
import Config
import json
import datetime
from bs4 import BeautifulSoup
from Album import Album

class AlbumManager:

    def __init__(self, spider, userID, ownerID):
        self.url = Config.ALBUMLISTURL  % ownerID
        self.spider = spider
        self.userID = userID
        self.ownerID = ownerID
        self.albumList = []  #list变量存储每一个album信息对象

    def getAllAlbumList(self):
        soup = BeautifulSoup(self.spider.getContent(self.url))
        '''
            chrome中打开相册链接，在Chrome开发者工具中element选项下可以看到
            该页面的html代码，在head标签页下的一个script标签页下可以找到所有的照片数据，下面
            就是找到该标签，进而得到照片数据
        '''
        for item in soup.find_all('script', type='text/javascript'):
        	#找到相册对应javascript则进行处理，处理完毕之后退出循环
            if 'nx.data.photo' in item.getText():
                rawContent = item.getText()
                #Json将JavaScript对象中表示的一组数据转换为字符串，之后可以方便在函数之间传递以处理。
                dictInfo = CommonFunction.generateJson(rawContent)	
                self.albumCount = dictInfo['albumList']['albumCount']
                for album in dictInfo['albumList']['albumList']:
                    info = {}  #dictionary变量存储album信息
                    info['albumId'] = album['albumId']
                    info['albumName'] = album['albumName']
                    info['photoCount'] = album['photoCount']
                    self.albumList.append(info)
                break;
        print ('**************All the album info has been obtained')

    def saveAlbum(self, album):
        name = album['albumName'].replace('/', '_') #替换不满足路径规则的字符
        path = Config.DATAPATH + '/' + self.ownerID + '/' + Config.ALBUMLISTPATH + '/' + album['albumId'] + '_' + name
        CommonFunction.CreatePath(path)
        album = Album(self.spider, self.userID, self.ownerID, album['albumId'], name, album['photoCount'], path)
        album.work()

    def work(self):
        self.getAllAlbumList()
        startDateTime = datetime.datetime.now()
        for album in self.albumList:
            self.saveAlbum(album)
        endDateTime = datetime.datetime.now()
        print ('all albums have been saved successfully, using time: ', endDateTime - startDateTime)	



