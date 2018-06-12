# -*- coding: utf-8 -*-

import Config
import CommonFunction
import datetime
from Photos import Photos
from bs4 import BeautifulSoup
from Comment import Comment

class Album:

    def __init__(self, spider, userID, ownerID, albumID, albumName, photoCount, path):
        self.url = Config.ALBUMURL % (ownerID, albumID)
        self.spider = spider
        self.userID = userID
        self.ownerID = ownerID
        self.albumID = albumID
        self.albumName = albumName
        self.photoCount = photoCount
        self.path = path
        self.photoList = []

    #方法同AlbumManager中的getAllAlbumList()，看那里的注释就好了
    def getPhotoList(self):
        #服务器返回的是html格式数据，不是json格式，需要查询获得html中需要的json数据
        #因此要使用BeautifulSoup()从HTML或XML文件中提取所需的json数据，
        #beautifulsoup自动将输入文档转换为Unicode编码，输出文档转换为utf-8编码。得到一个BeautifulSoup的对象, 
        soup = BeautifulSoup(self.spider.getContent(self.url))
        for item in soup.find_all('script', type = 'text/javascript'):
            if 'nx.data.photo' in item.getText():
                rawContent = item.getText()
                dictInfo = CommonFunction.generateJson(rawContent)
                for photo in dictInfo['photoList']['photoList']:
                    info = {}
                    info['albumId'] = photo['albumId']
                    info['photoId'] = photo['photoId']
                    info['ownerId'] = photo['ownerId']
                    self.photoList.append(info)
                break

    def getAlbumComments(self):
        comment = Comment(self.spider, self.userID, self.albumID, 'album', self.ownerID)
        content = comment.work()
        if content != '':
            with open(self.path + '/comments.markdown','wb') as f:
                f.write((u'******评论： ******\n\n').encode('utf-8'))
                f.write(content)

    def savePhotos(self):
        for item in self.photoList:
            photos = Photos(self.spider, self.userID, self.albumName, item, self.path)
            photos.work()
            break  #通过一张照片的信息就可以在element页面下的html代码中得到该相册所有照片，所以不用遍历每一个照片信息了

    def work(self):
        self.getPhotoList()
        self.getAlbumComments()
        print (datetime.datetime.now(), self.albumName, 'is downloadinig...')
        self.savePhotos()
        print (datetime.datetime.now(), self.albumName, 'saves successfully!')    	



