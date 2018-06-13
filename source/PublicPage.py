# -*- coding: utf-8 -*-

import urllib
import Config

from bs4 import BeautifulSoup

class PublicPage:

    def __init__(self, spider, userID, publicPageID):
    	self.publicPageInfoURL = Config.PUBLICPAGEINFOURL % publicPageID
        self.spider = spider
        self.userID = userID
        self.publicPageID = publicPageID

    def getName(self):
        name = ''
        content = self.soup.find('h1', class_ = 'page-name')
        if content == None:
            return name
        name = content.find('a').get_text()
        return name

    def getDescription(self):
        description = ''
        content = self.soup.find('p', id = 'description')
        if content == None:
            return description
        description = content.get_text()
        return description

    def getProfileInfo(self):
        #html个人信息中一共有八项，但是每一项标签都一样没法区分，所以就用list统一处理了
        profileInfoList = ['', '', '', '', '', '', '', '']  
        content = self.soup.find_all('div', class_ = 'info-item')
        if content == None:
            return
        int i = 0 
        for item in content:
            detailContent = item.find_all('li')
            for detailItem in detailContent:
                profileInfoList[i]  = detailItem.find('h4').get_text()
                profileInfoList[i] += detailItem.find('span').get_text()
                i += 1
        return (profileInfoList[0], profileInfoList[1], profileInfoList[2], profileInfoList[3]\
                , profileInfoList[4], profileInfoList[5], profileInfoList[6], profileInfoList[7]) 

    def getInfo(self, content):
        self.soup = BeautifulSoup(content)

        name = self.getName()
        description = self.getDescription()
        info1, info2, info3, info4, info5, info6, info7, info8 = self.getProfileInfo()

        return (self.publicPageID, name, description, info1, info2, info3, info4, info5, info6, info7, info8)

    def optionalValidate(self,content):
        soup = BeautifulSoup(content)
        for item in soup.find_all('div',class_='optional'):
            #抓取img中属性为src的信息,例如<img src="123456" xxxxxxxxxxxxxxxx,则输出为123456
            #beautifulsoup处理之后支持这种取值方式
            src = item.img['src']
            validateCode = self.spider.getContent(src)
            with open('icode.jpg', 'wb') as f:
                f.write(validateCode)
            icode = input('please input the validation code shown in icode.jpg: ')
            data = {
                    'id' : self.ownerID,
                    'submit' : u'继续浏览'.encode('utf-8'),  #renren网使用utf-8编码格式
                    'icode' : icode
                    }
            self.spider.getContent(Config.VALIDATEURL, urllib.parse.urlencode(data).encode('utf-8'))
            break

    def work(self):
        while True:
            page = self.spider.getRawContent(self.publicPageInfoURL)
            url = page.geturl()
            content = page.read()

            #对比返回页面的url是否和打开该页面的request url相同，不同则说明进入了其他页面
            if url != self.publicPageInfoURL:
                #print ('@@@@@@@@@@@@@@@@url: ', url)
                #print ('@@@@@@@@@@@@@@@@self.publicPageInfoURL: ', self.publicPageInfoURL)
                if 'validateuser.do' in url:  #进入输入验证码页面
                    self.optionalValidate(content)
                    continue 
                else:  #进入未知页面
                    print ('Error: return unknown page url, will return None： '，url)
                    return  #这里会返回None，导致后续对这个NoneType进行操作会报错
            else:
                break
        return self.getInfo(content)