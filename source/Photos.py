# -*- coding: utf-8 -*-

import Config
import CommonFunction
import urllib
from Comment import Comment
from bs4 import BeautifulSoup

class Photos:

    def __init__(self, spider, userID, albumName, summary, path):
        self.spider = spider
        self.userID = userID
        self.albumName = albumName
        self.ownerID = summary['ownerId']
        self.albumID = summary['albumId']
        self.pageURL = Config.PHOTOSURL % (self.ownerID, summary['photoId'])
        self.photos = []
        self.path = path

    #通过一张照片的页面就可以获得该相册所有照片的信息
    def getPhotoDetailList(self):
        #服务器返回的是html格式数据，不是json格式，需要查询获得html中需要的json数据
        #因此要使用BeautifulSoup()从HTML或XML文件中提取所需的json数据，
        #beautifulsoup自动将输入文档转换为Unicode编码，输出文档转换为utf-8编码。得到一个BeautifulSoup的对象, 
        soup = BeautifulSoup(self.spider.getContent(self.pageURL))
        for item in soup.find_all('script', type = 'text/javascript'):
            if 'nx.data.photo' in item.getText():
                rawContent = item.getText()
                dictInfo = CommonFunction.generateJson(rawContent)
                self.photoCount = dictInfo['photoTerminal']['json']['photoNum']
                for item in dictInfo['photoTerminal']['json']['list']:
                    info = {}
                    info['id'] = int(item['id'])
                    info['title'] = item['originTitle']
                    info['date'] = item['date']
                    if item['xLargeUrl']:
                        info['url'] = item['xLargeUrl']
                    else:
                        info['url'] = item['large480']
                    info['commentCount'] = item['commentCount']
                    info['owner'] = item['owner']
                    self.photos.append(info)   
                break

    def savePhotos(self):
        for item in self.photos:
            filename = self.path + '/' + str(item['id']) + '.jpg'
            count = 0
            if CommonFunction.IsPathExist(filename) == False:  #如果该照片已经存在则不创建，为了节省程序运行时间
                with open(filename, 'wb') as f:
                    while True:
                        try:
                            opener = urllib.request.build_opener()  #构建简单的opener
                            #Spider.py中还有另外一中设置header内容的写法
                            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')]
                            urllib.request.install_opener(opener)
                            urllib.request.urlretrieve(item['url'], filename)  #将照片从远程数据下载到本地
                        except Exception as e:
                            print (item['id'], 'fail + 1', e)
                            count += 1
                        else:
                            count = 0
                            break
                    #评论comment可以用类似方式，就是通过url获得content之后，解吗json数据，但是照片不行
                    #f.write(self.spider.getContent(item['url']))   
    def savePhotoComment(self):
        with open(self.path + '/photo_detail.markdown', 'wb') as f:
            for item in self.photos:
                f.write(Config.GAP.encode('utf-8'))

                line = '***Photo ID: ' + str(item['id']) + '***\n\n'
                line += '***Photo Name: ' + item['title'].replace('\n', ' ') + '***\n\n'
                line += '*** Photo Time: ' + item['date'] + '***\n\n'
                f.write(line.encode('utf-8'))  #转为utf-8编码格式
                filename = str(item['id'])
                f.write(('Photo File Name: ' + filename + '.jpg\n\n').encode('utf-8'))
                if int(item['commentCount']):
                    comment = Comment(self.spider, self.userID, item['id'], 'photo', item['owner'])
                    f.write((u'***评论: ***\n\n').encode('utf-8'))  #字符串前面加u也是将编码变为utf-8，但是后面已经转码了，所以没有必要其实
                    f.write(comment.work())
                    
                f.write(Config.GAP.encode('utf-8'))

    def work(self):
        self.getPhotoDetailList()
        self.savePhotos()
        self.savePhotoComment()    	



