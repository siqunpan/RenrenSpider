# -*- coding: utf-8 -*-

import urllib
import json
import Config
import datetime

from Comment import Comment
from bs4 import BeautifulSoup

class Status:

    def __init__(self, spider, userID, ownerID):
        self.url = Config.STATUSURL
        self.userID = userID
        self.spider = spider
        self.ownerID = ownerID
        self.status = []

    def getStatusURL(self, pageNo = 0):
        data = {
                'userId': self.ownerID,
                'curpage': pageNo
                }
        return self.url + '?' + urllib.parse.urlencode(data)

    def setContent(self, content):
        dictInfo = json.loads(content)
        '''
            以下dictionary中的key值信息是通过打印出服务器返回的content，分析其内容得到的
            
            json.loads()用于将str类型的数据转成dictionary

            当我们用requests请求一个返回json的接口时候，得到的结果中包含了一串让人看
            不懂的东西 \\uxxxx的，这是中文对应的unicode编码形式。json.loads()就可以把他们转化为中文
        '''
        if dictInfo['doingArray'] == []:
            return  False
        for item in dictInfo['doingArray']:
            info = {}
            info['id'] = int(item['id'])
            info['dtime'] = item['dtime']
            info['comment_count'] = item['comment_count']
            info['content'] = item['content']
            key = 'rootDoingUserName'
            if key in item:
                info['rootDoingUserName'] = item['rootDoingUserName']
                info['rootContent'] = item['rootContent']
            else:
                info['rootDoingUserName'] = ''
                info['rootContent'] = ''
            self.status.append(info)
        return True

    def getStatusList(self):
        return self.status

    def saveContent(self):
        self.statusCount = len(self.status)
        with open(Config.DATAPATH + '/' + self.ownerID + '/status.markdown', 'wb') as f:
            f.write(Config.GAP.encode('utf-8'))
            str1 = u'status总数量: ' + str(self.statusCount) + '\n'
            f.write(str1.encode('utf-8'))
            f.write(Config.GAP.encode('utf-8'))
            for item in self.status:
                line = u'*** ID号: ***' + str(item['id']) + '\n'
                line += u'*** 发表时间: ***' + item['dtime'] + '\n'
                line += u'*** 评论数: ***' + str(item['comment_count']) + '\n\n'
                line += u'*** 内容: ***' + item['content'] + '\n\n'
                #line += u'*** 内容: ***' + BeautifulSoup(item['content']).getText() + '\n\n'  #另一种方法
                line += u'*** 原作者: ***' + item['rootDoingUserName'] + '\n\n'
                line += u'*** 原内容: ***' + item['rootContent'] + '\n\n'
                f.write(line.encode('utf-8'))
                if int(item['comment_count']):
                    f.write((u'*** 评论: ***\n\n').encode('utf-8'))
                    comments = Comment(self.spider, self.userID,item['id'], 'status', self.ownerID)
                    f.write(comments.work())
                f.write(Config.GAP.encode('utf-8'))
        print(datetime.datetime.now(), ': status save successfully')	

    def work(self):
        pageNo = 0
        while True:
            result = self.setContent(self.spider.getContent(self.getStatusURL(pageNo)))
            pageNo += 1
            if result == False:
                break
        self.saveContent()    	