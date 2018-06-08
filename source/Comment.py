# -*- coding: utf-8 -*-

import urllib
import json
import Config

class Comment:

    def __init__(self, spider, userID, entryID, sourceType, ownerID):
        self.url = Config.COMMENTURL
        self.spider = spider
        self.userID = userID
        self.entryID = entryID
        self.sourceType = sourceType
        self.ownerID = ownerID
        self.comments = []

    def getCommentURL(self, offset = 0):
        data = {
                'limit' : 20,
                'desc' : 'false',
                'offset' : offset,
                'replaceUBBLarge' : 'true',
                'type' : self.sourceType,
                'entryId' : self.entryID,
                'entryOwnerId' : self.ownerID
                }
        return self.url + '?' + urllib.parse.urlencode(data)

    def setContent(self, content):
        #print ('**********str content begin**********')
        #print (content)
        #print ('**********str content end************')
        dictinfo = json.loads(content)
        #print ('**********dict content begin**********')
        #print (content)
        #print ('**********dict content end************')
        
        '''
            以下dictionary中的key值信息是通过打印出服务器返回的content，分析其内容得到的
            
            json.loads()用于将str类型的数据转成dictionary

            当我们用requests请求一个返回json的接口时候，得到的结果中包含了一串让人看
            不懂的东西 \\uxxxx的，这是中文对应的unicode编码形式。json.loads()就可以把他们转化为中文
        '''
        dictInfo = json.loads(content) 
        for item in dictInfo['comments']:
            info = {}
            info['type'] = item['type']
            info['id'] = item['id']
            info['time'] = item['time']
            info['authorName'] = item['authorName']
            info['authorId'] = item['authorId']
            info['content'] = item['content']
            self.comments.append(info)
        return (dictInfo['hasMore'], dictInfo['nextOffset'])

    #获得所需评论信息
    def saveContent(self):
        lines = '\n'
        for item in self.comments:
            lines += item['authorName'] + '    ' + item['time'] + '\n\n'
            line = item['content'].replace('\n','')
            line = line.replace('\r', '')
            lines += '*' + line + '*\n\n'
        return lines.encode('utf-8')  #需要转为utf-8编码格式   

    def work(self):
        offset = 0
        while True:
            result = self.setContent(self.spider.getContent(self.getCommentURL(offset)))
            hasMore, nextOffset = result
            if hasMore:
                offset = nextOffset
            else:
                break
        return self.saveContent()	

