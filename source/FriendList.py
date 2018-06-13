# -*- coding: utf-8 -*-

import Config
import json
from PersonalInfo import PersonalInfo

class FriendList:

    def __init__(self, spider):
        self.url = Config.FRIENDLISTURL
        self.spider = spider
        self.friendList = []

    def getFriendListURL(self):
        return self.url

    '''
        返回数据不满足json格式，因此需要先手动找到"data"部分数据，之后将数据修正以满足json格式，再进行处理
    '''
    def setContent(self, content):
        strData = '"data"'.encode('utf-8')  #所有朋友信息的标志字符串
        beginIndex = content.find(strData)  #content是string类型，返回content中包含strData的起始索引
        
        #返回content字符串中从beginIndex到倒数第3个字符的字符串，即"data"的数据
        content = content[beginIndex:-3].decode()  
        
        strDataMatchedJson = '{' + content + '}'  #补全最外层大括号以满足json数据格式要求

        #将满足json格式要求的string转化为json格式以方便处理，并且string中的ASC||编码也会被解码成汉字
        dictInfo = json.loads(strDataMatchedJson)  
        
        self.friendsNum = dictInfo['data']['hostFriendCount']  #除了遍历friends，'hostFriendCount'属性也能获得好友数量
        for item in dictInfo['data']['friends']:
            info = {}
            #当有多个分组时，暂时只取第一个分组，之后再加上第二个组
            if len(item['fgroups']) == 0:
                firstGroup = u'无分组'
                secondGroup = u'无第二分组'
            elif len(item['fgroups']) == 1:
                firstGroup = item['fgroups'][0]  
                secondGroup = u'无第二分组'
            elif len(item['fgroups']) == 2:
                firstGroup = item['fgroups'][0]
                secondGroup = item['fgroups'][1] 
            info['firstGroup'] = firstGroup
            info['secondGroup'] = secondGroup
            info['fid'] = item['fid']
            info['comf'] = item['comf']
            info['fname'] = item['fname']
            info['belong'] = item['info']
            self.friendList.append(info)

#     def saveContent(self): 
#         for item in self.friendList:
#             print item['firstGroup'], item['secondGroup'] item['fid'], item['comf'], item['fname'], item['belong']

    def work(self):
        self.setContent(self.spider.getContent(self.url))
        return self.friendList