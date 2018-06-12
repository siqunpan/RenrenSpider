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
        #服务器返回的是html格式数据，不是json格式，需要查询获得html中需要的json数据
        #因此要使用BeautifulSoup()从HTML或XML文件中提取所需的json数据，
        #beautifulsoup自动将输入文档转换为Unicode编码，输出文档转换为utf-8编码。得到一个BeautifulSoup的对象, 
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
                #将所需数据中不满足json格式部分修整，并将json格式字符串转换为python的dictionary格式
                dictInfo = CommonFunction.generateJson(rawContent)	

                '''
                    在使用json.load()获得python的dictionary格式数据之后，知道dictionary中的key值信息有两种方式：
                        通过print()函数打印出服务器返回的content
                        如果服务器返回的数据是json格式，则将google开发者工具中network，中捕获的数据中的request url
                            输入到网址栏，就可以看到范返回数据。
                            但是如果服务器返回的是数据是html格式字，json数据是通过beautifulsoup对象查询获得，这种情况下
                            这个第二种方法就不适用，只能适用打印信息的方法
                '''
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



