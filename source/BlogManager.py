# -*- coding:utf-8 -*-

import urllib
import json
import Config
import datetime
import CommonFunction

from Comment import Comment
from Blog import Blog

class BlogManager:

    def __init__(self, spider, userID, ownerID):
        self.url = Config.BLOGLISTURL % ownerID
        self.spider = spider
        self.userID = userID
        self.ownerID = ownerID
        self.blogsCount = 0
        self.blogList = []

    def getBlogListURL(self, categoryId = 0, pageNo = 0):
        data = {
                'categoryId' : categoryId,
                'curpage' : pageNo,   
                }
        return self.url + urllib.parse.urlencode(data)

    def setContent(self, content):
        '''
            以下dictionary中的key值信息是通过打印出服务器返回的content，分析其内容得到的
            
            json.loads()用于将str类型的数据转成dictionary

            当我们用requests请求一个返回json的接口时候，得到的结果中包含了一串让人看
            不懂的东西 \\uxxxx的，这是中文对应的unicode编码形式。json.loads()就可以把他们转化为中文
        '''
        #print (*********Before Json.loads(content)*************)
        #print (content)
        dictInfo = json.loads(content)
        #print (*********After Json.loads(content)*************)
        #print (content)
        self.blogsCount = dictInfo['count']
        for item in dictInfo['data']:
            info = {}
            #一定都是2000年之后些的日志
            info['createTime'] = '20' + item['createTime']
            info['commentCount'] = item['commentCount']
            info['id'] = int(item['id'])
            info['title'] = item['title']
            info['category'] = item['category']
            info['containAudio'] = item['containAudio']
            info['containImage'] = item['containImage']
            info['containVideo'] = item['containVideo']
            self.blogList.append(info)
        if self.blogsCount - len(self.blogList) > 0:
            return True
        else:
            return False

    def saveContent(self):
        with open(Config.DATAPATH + '/' + self.ownerID + '/blogList.markdown', 'wb') as f:
            str1 = str(self.blogsCount) + '\n'
            f.write(str1.encode('utf-8'))
            f.write(Config.GAP.encode('utf-8'))
            for item in self.blogList:
                line  = 'blog id: ' + str(item['id']) + '\n\n'
                line += 'createTime: ' + item['createTime'] + '\n\n'
                line += 'category: ' + item['category'] + '\n\n'
                line += 'title: ' + item['title'] + '\n\n'
                line += 'commentCount: ' + str(item['commentCount']) + '\n\n'
                line += 'containImage: ' + str(item['containImage']) + '\n\n'
                line += 'containAudio: ' + str(item['containAudio']) + '\n\n'
                line += 'containVideo: ' + str(item['containVideo']) + '\n\n'
                line += Config.GAP
                f.write(line.encode('utf-8'))
        print (datetime.datetime.now(), ': blogList saves successfully')
        
    def saveEveryBlog(self):
        startDatetime = datetime.datetime.now()
        for item in self.blogList:
            blogID = str(item['id'])
            filename = Config.DATAPATH + '/' + self.ownerID + '/' + Config.BLOGPATH + \
                         '/' + item['createTime'] + '_' + item['category'] + '_' + item['title'] + '.markdown'
            legalName = CommonFunction.validateFilename(filename)  #获取的文件名字含有不符合路径要求的字符，需要被替换
            blog = Blog(self.spider, self.userID, self.ownerID, blogID, legalName, item)
            blog.work()
        endDatetime = datetime.datetime.now()
        print('all blogs have been downloaded successfully with time: ', endDatetime - startDatetime)

    def work(self):
        i = 0
        while True:
            result = self.setContent(self.spider.getContent(self.getBlogListURL(pageNo=i)))
            i += 1
            if result == False:
                break
        self.saveContent()
        self.saveEveryBlog()           






