# -*- coding: utf-8 -*-

import urllib
import json
import Config
import CommonFunction

class ChatList:

    def __init__(self, spider, summary):
        self.chatUrl = Config.CHATURL
        self.spider = spider
        self.friendUid = summary['uid']
        self.friendName = summary['name']
        self.chatList = []

    def getChatListURL(self, st, lt):
        data = {
                'lt': lt,  #页面显示聊天数量，比如st是10，it是20，则从第11条聊天开始显示到第21条聊天，如果总数不足则显示到最后
                'st': st,  #从st的下一个开始显示，比如st是10，则从第11条聊天开始显示
                'type': 0,  #type为1时候是一些公众号聊天，暂时不处理，只处理好友聊天
                'roomId': self.friendUid,
                }
        return self.chatUrl + '?' + urllib.parse.urlencode(data)	

    def setChatListContent(self, content):
        #print ('*********content of chatlist content: ', content)
        dictInfo = json.loads(content)
        for item in dictInfo['data']['items']:
            info = {}
            info['content'] = item['content']
            info['fromId'] = str(item['fromId'])
            info['fromName'] = item['fromName']
            datetime = CommonFunction.timestampToLocaltime(item['time'])  #将时间戳转化为本地时间
            info['time'] = datetime

            # print ('*************item[\'fromId\'], item[\'fromName\']: ', item['fromId'], item['fromName'])
            # print ('*************item[\'content\']: ', item['content'])

            self.chatList.append(info)
        if len(dictInfo['data']['items']) > 0:
            return True
        else:
            return False       

    def work(self):
        i = 0
        showNumEachPage = 20  #当前页显示多少条聊天
        while True:
            st = i*showNumEachPage  #从st的下一个开始显示，比如st是10，则从第11条聊天开始显示
            lt = showNumEachPage  #页面显示聊天数量，比如st是10，it是20，则从第11条聊天开始显示到第21条聊天，如果总数不足则显示到最后
            result = self.setChatListContent(self.spider.getContent(self.getChatListURL(st, lt)))
            i += 1
            if result == False:
                break
        return self.chatList


