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

    def setContent(self, content):
        strData = '"data"'.encode('utf-8')  #所有朋友信息的标志字符串
        beginIndex = content.find(strData)  #content是string类型，返回content中包含strData的起始索引
        content = content[beginIndex:-3].decode()  #返回content字符串中从beginIndex到倒数第3个字符的字符串，即"data"的数据
        strDataMatchedJson = '{' + content + '}'  #补全最外层大括号以满足json数据格式要求
        dictInfo = json.loads(strDataMatchedJson)  #将满足json格式要求的string转化为json格式以方便处理，并且string中的ASC||编码也会被解码成汉字
        self.friendsNum = dictInfo['data']['hostFriendCount']  #除了遍历friends，'hostFriendCount'属性也能获得好友数量
        for item in dictInfo['data']['friends']:
            info = {}
            #当有多个分组时，暂时只取第一个分组，之后再加上第二个组
            if len(item['fgroups']) == 0:
                firstGroup = u'无分组'
            elif len(item['fgroups']) == 1:
                firstGroup = item['fgroups'][0]  
                secondGroup = u'无第二分组'
            elif len(item['fgroups']) == 2:
                firstGroup = item['fgroups'][0]
                secondGroup = item['fgroups'][1] 
            info['firstGroup'] = firstGroup
            info['fid'] = item['fid']
            info['comf'] = item['comf']
            info['fname'] = item['fname']
            info['belong'] = item['info']
            self.friendList.append(info)

#     def saveContent(self): 
#         for item in self.friendList:
#             print item['firstGroup'], item['fid'], item['comf'], item['fname'], item['belong']

    def work(self):
        self.setContent(self.spider.getContent(self.url))
        return self.friendList