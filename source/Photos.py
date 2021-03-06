# -*- coding: utf-8 -*-

import Config
import CommonFunction
import urllib
from Comment import Comment
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests
import PrivateConfig
import re
import time

class Photos:

    def __init__(self, spider, userID, albumName, summary, path, onlyDownloadPhotoReal = False):
        self.spider = spider
        self.userID = userID
        self.albumName = albumName
        self.ownerID = summary['ownerId']
        self.albumID = summary['albumId']
        self.pageURL = Config.PHOTOSURL % (self.ownerID, summary['photoId'])
        self.photos = []
        self.path = path
        self.onlyDownloadPhotoReal = onlyDownloadPhotoReal
        self.curPhotoID = summary['photoId']
        self.popupPhotoURL = Config.POPUPPHOTOURL % (self.ownerID, self.albumID, self.ownerID, self.curPhotoID)
        self.driver = None

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

    def getAllPhotosInfoInAlbum(self):
        self.getPhotoDetailList()
        return self.photos

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

    def getCookies(self, url, account, password):
        '''通过request 登陆，获取cookie'''
        data = {
                'email' : account,
                'password' : password,
                'origURL' : 'http://www.renren.com/home',
                'icode' : ''
        }

        cookiesList = []
        roomSession  = requests.Session()
        roomSession.post(url,data=data)
        loadCookies = requests.utils.dict_from_cookiejar(roomSession.cookies)
        for cookieName,cookieValue in loadCookies.items():
            cookies = {}
            cookies['name'] = cookieName
            cookies['value'] = cookieValue
            cookiesList.append(cookies)

        return cookiesList

    def tryLogin(self, requestUrl):
        '''判断是否登陆状态，非登陆状态,通过cookie登陆'''
        self.driver.get(requestUrl) #测试是否为登陆状态
        if '注册' in self.driver.page_source:  #判断是否登陆为登陆页面
            for cookie in self.getCookies(Config.LOGINURL,PrivateConfig.Email,PrivateConfig.Password): #如果登陆界面获取cookie
                self.driver.add_cookie(cookie)  #添加cookie ，通过Cookie登陆

    def getPopupPhotoURL(self):
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")

        if self.driver == None:
            chromeOptions = Options()
            chromeOptions.add_argument("--headless")

            chromedriverPath = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromedriverPath
            self.driver = webdriver.Chrome(executable_path = chromedriverPath, chrome_options = chromeOptions)
            self.tryLogin(self.popupPhotoURL)

        self.driver.get(self.popupPhotoURL) 
        soup = BeautifulSoup(self.driver.page_source) 

        imgPopupContent = soup.find(name='img', class_ = 'pop-content-img viewer-img-show')
        if imgPopupContent != None:
            print('*****************imgPopupContent, and src: ', imgPopupContent, ', ', imgPopupContent.get('src'))
        else:
            print('*****************imgPopupContent is None!!!')

        if imgPopupContent != None and imgPopupContent.get('src') != None:
            self.urlPopup = imgPopupContent.get('src')
        else:
            self.urlPopup = None

    def getPhotoRealURL(self):
        if self.driver == None:
            chromeOptions = Options()
            chromeOptions.add_argument("--headless")

            chromedriverPath = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromedriverPath
            self.driver = webdriver.Chrome(executable_path = chromedriverPath, chrome_options = chromeOptions)
            self.tryLogin(self.pageURL)

        self.driver.get(self.pageURL) 

        soup = BeautifulSoup(self.driver.page_source)

        imgContent = soup.find(name='img', class_ = 'photo-item photo-item-cur')
        if imgContent != None:
            print('*****************imgContent, and src: ', imgContent, ', ', imgContent.get('src'))
        else:
            print('*****************imgContent is None!!!')

        if imgContent != None and imgContent.get('src') != None:
            self.urlShown = imgContent.get('src')
        else:    #有时候链接失效，因此需要使用popup的url
            self.getPopupPhotoURL()
            self.urlShown = None

        imgContentPre = soup.find(name='img', class_ = 'photo-item photo-item-pre')
        if imgContentPre != None and imgContentPre.get('id') != "":
            imgIdStrPre = imgContentPre.get('id')
            pattern = r'\d+'

            self.prePhotoID = (re.search(pattern, imgIdStrPre)).group()
        else:
            print('*****************imgContentPre is None!!!')

        if imgContentPre != None and imgContentPre.get('src') != None:
            self.urlShownPre = imgContentPre.get('src')
        else:
            self.urlShownPre = None

        imgContentNext = soup.find(name='img', class_ = 'photo-item photo-item-next')
        if imgContentNext != None and imgContentNext.get('id') != "":
            imgIdStrNext = imgContentNext.get('id')
            pattern = r'\d+'

            self.nextPhotoID = re.search(pattern, imgIdStrNext).group()
        else:
            print('*****************imgContentNext is None!!!')

        if imgContentNext != None and imgContentNext.get('src') != None:
            self.urlShownNext = imgContentNext.get('src')
        else:
            self.urlShownNext = None

        # content = soup.find_all('div', class_ = 'photo-list')
        # for item in content:
        #     #print('*****************getPhotoRealURL content: ', item)
        #     #print('*****************getPhotoRealURL: ', item.img['src'])
        #     if content == None:
        #         print('*****************getPhotoRealURL is None')
        #     self.urlShown = item.img['src']
        #     print('*****************self.urlShown of photo real: ', self.urlShown) 

    def savePhotoReal(self):
        if self.urlShown == None:
            if self.urlPopup == None:
                return
            else:
                self.urlShown = self.urlPopup

        filename = self.path + '/' + str(self.curPhotoID) + '_shown' + '.jpg'

        count = 0
        if CommonFunction.IsPathExist(filename) == False:  #如果该照片已经存在则不创建，为了节省程序运行时间
            with open(filename, 'wb') as f:
                while True:
                    try:
                        opener = urllib.request.build_opener()  #构建简单的opener
                        #Spider.py中还有另外一中设置header内容的写法
                        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')]
                        urllib.request.install_opener(opener)
                        urllib.request.urlretrieve(self.urlShown, filename)  #将照片从远程数据下载到本地
                        print ('********************download photo shown in page successfully: ', self.urlShown)
                    except Exception as e:
                        print (item['id'], 'fail + 1', e)
                        count += 1
                    else:
                        count = 0
                        break
                #f.write(self.spider.getContent(item['url']))  

    def savePhotoRealPre(self):
        if self.urlShownPre == None:
            return

        filename = self.path + '/' + str(self.prePhotoID) + '_shown' + '.jpg'

        count = 0
        if CommonFunction.IsPathExist(filename) == False:  #如果该照片已经存在则不创建，为了节省程序运行时间
            with open(filename, 'wb') as f:
                while True:
                    try:
                        opener = urllib.request.build_opener()  #构建简单的opener
                        #Spider.py中还有另外一中设置header内容的写法
                        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')]
                        urllib.request.install_opener(opener)
                        urllib.request.urlretrieve(self.urlShownPre, filename)  #将照片从远程数据下载到本地
                        print ('********************download photo shown in page successfully: ', self.urlShownPre)
                    except Exception as e:
                        print (item['id'], 'fail + 1', e)
                        count += 1
                    else:
                        count = 0
                        break
                #f.write(self.spider.getContent(item['url']))  

    def savePhotoRealNext(self):
        if self.urlShownNext == None:
            return

        filename = self.path + '/' + str(self.nextPhotoID) + '_shown' + '.jpg'

        count = 0
        if CommonFunction.IsPathExist(filename) == False:  #如果该照片已经存在则不创建，为了节省程序运行时间
            with open(filename, 'wb') as f:
                while True:
                    try:
                        opener = urllib.request.build_opener()  #构建简单的opener
                        #Spider.py中还有另外一中设置header内容的写法
                        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')]
                        urllib.request.install_opener(opener)
                        urllib.request.urlretrieve(self.urlShownNext, filename)  #将照片从远程数据下载到本地
                        print ('********************download photo shown in page successfully: ', self.urlShownNext)
                    except Exception as e:
                        print (item['id'], 'fail + 1', e)
                        count += 1
                    else:
                        count = 0
                        break
                #f.write(self.spider.getContent(item['url']))  

    def work(self):
        if self.onlyDownloadPhotoReal == False:
            self.getPhotoDetailList()
            self.savePhotos()
            self.savePhotoComment()
        else:  
            filename = self.path + '/' + str(self.curPhotoID) + '_shown' + '.jpg'
            print ('********************filename of photo: ', filename)
            if CommonFunction.IsPathExist(filename) == False:  #如果该照片已经存在则不创建，为了节省程序运行时间
                print ('***********get and download photo: ', filename)
                self.getPhotoRealURL()
                self.savePhotoReal()
                self.savePhotoRealPre()
                self.savePhotoRealNext()




