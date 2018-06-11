# -*- coding: utf-8 -*-

import urllib
import json
import Config

from Chat import Chat

class Chat:

    def __init__(self, spider, userID, ownerID):
        self.friendSimpleInfoUrl = Config.FRIENDLISTURLNEW  #仅用于获取聊天信息所需要的好友基本信息：ID和名字
        self.spider = spider
        self.userID = userID
        self.ownerID = ownerID
        self.friendsCount = 0
        self.friendSimpleInfoList = []
        self.chatList = []

    def getFriendListForChatURL(self, st, lt):
        data = {
                'st': st,  #从st的下一个开始显示，比如st是100，则从101号好友开始显示
                'lt': lt,  #页面显示好友信息数量，比如st是100，lt是20，则从101开始显示到121号好友，如果总数不足则显示到最后
                }
        return self.friendSimpleInfoUrl + '?' + urllib.parse.urlencode(data)

    def setFriendSimpleInfoContent(self, content):
        #print ('*********content of friendlist info content for chat: ', content)
        dictInfo = json.loads(content)
        self.friendsCount = dictInfo['data']['total']
        for item in dictInfo['data']['items']:
            info = {}
            info['uid'] = int(item['uid'])
            info['name'] = item['name']
            self.friendSimpleInfoList.append(info)
        if len(dictInfo['data']['items']) > 0:
            return True
        else:
            return False

    def setChatContent(self):
        for item in self.friendSimpleInfoList:
            chat = Chat(self.spider, item)
            self.chatList.append(chat.work())


    def work(self):
        i = 0
        showNumEachPage = 50  #当前页显示多少个好友信息
        while True:
            st = i*showNumEachPage  #从st的下一个开始显示，比如st是100，则从101号好友开始显示
            lt = showNumEachPage  #页面显示好友信息数量，比如st是100，it是20，则从101开始显示到121号好友，如果总数不足则显示到最后
            result = self.setFriendSimpleInfoContent(self.spider.getContent(self.getFriendListForChatURL(st, lt)))
            i += 1
            if result == False:
                break
        self.setChatContent()
        #self.saveContent()	

