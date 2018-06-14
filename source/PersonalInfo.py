# -*- coding: utf-8 -*-

import urllib
import Config

from bs4 import BeautifulSoup

class PersonalInfo:
    
    def __init__(self, spider, userID, ownerID, summary=None):
        self.personalInfoURL =  Config.PERSONALINFOURL % ownerID
        self.spider = spider
        self.userID = userID
        self.ownerID = ownerID
        self.summary = summary

    def getContent(self, info):
        return self.soup.find('div', class_ = 'info-section clearfix', id = info)

    def getEduInfo(self, info):
        edu = ''
        if self.getContent(info) == None:
            return edu
        for item in self.getContent(info).find_all('dl', class_ = 'info'):
            #strip()当参数为空时（即括号里没东西），默认删除空白符（包括'\n', '\r', '\t', ' ')，
            #但是只能删除开头和结尾的，不能删除字符串中间的
            edu += item.find('dt').string + ':(' + item.find('dd').get_text().strip().replace('\n', '') + ') '
        return edu

    def getBasicInfo(self, info):
        gender, birth, hometown = '', '', ''
        if self.getContent(info) == None:
            return (gender, birth, hometown)
        for item in self.getContent(info).find_all('dl',class_='info'):
            if item.find('dt').string == u'性别':
                if item.find('dd').get_text().strip() == u'男':
                    gender = 'm'
                elif item.find('dd').get_text().strip() == u'女':
                    gender = 'f'
                else:
                    gender = 'u'
            elif item.find('dt').string == u'生日':
                birth = item.find('dd').get_text().strip().replace('\n','')
            elif item.find('dt').string == u'家乡':
                hometown = item.find('dd').get_text().strip().replace('\n','')       
        return (gender, birth, hometown)

    def getInfo(self, content):
        self.soup = BeautifulSoup(content)
        edu = self.getEduInfo('educationInfo')
        gender, birth, hometown = self.getBasicInfo('basicInfo')
        id = self.ownerID
        if self.userID == self.ownerID:

            #获得自己的名字
            myName = self.soup.find('a', class_ = 'hd-name').get_text()
            relation = 'myself'
            name, belong, firstGroup, secondGroup, comf = myName, '', '', '', ''
        else:
            relation = 'friend'
            name = self.summary['fname']
            belong = self.summary['belong']
            firstGroup = self.summary['firstGroup']
            secondGroup = self.summary['secondGroup']
            comf = self.summary['comf']
        return (id,name,relation,gender,birth,hometown,belong,firstGroup,secondGroup,edu,comf)  

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
            page = self.spider.getRawContent(self.personalInfoURL)
            url = page.geturl()
            content = page.read()

            #对比返回页面的url是否和打开该页面的request url相同，不同则说明进入了其他页面
            if url != self.personalInfoURL:
                #print ('@@@@@@@@@@@@@@@@url: ', url)
                #print ('@@@@@@@@@@@@@@@@self.personalInfoURL: ', self.personalInfoURL)
                if 'validateuser.do' in url:  #进入输入验证码页面
                    self.optionalValidate(content)
                    continue
                elif 'page.renren.com' in url:  #该好友是公共主页，进入公共主页页面
                    return 'public page' 
                else:  #进入未知页面
                    print ('Error: return unknown page url, will return None： ', url)
                    return  #这里会返回None，导致后续对这个NoneType进行操作会报错
            else:
                break
        return self.getInfo(content)

