# -*- coding: utf-8 -*-

import urllib
import json
import Config

from ChatList import ChatList

class ChatManager:

    def __init__(self, spider, userID, ownerID):
        self.friendSimpleInfoUrl = Config.FRIENDLISTURLNEW  #仅用于获取聊天信息所需要的好友基本信息：ID和名字
        self.chatfilePath = Config.DATAPATH + '/' + ownerID + '/' + Config.ChatFile
        self.spider = spider
        self.userID = userID
        self.ownerID = ownerID
        self.friendsCount = 0
        self.friendSimpleInfoList = []
        self.allChatLists = []

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

    def setAllChatListsContent(self):
        for item in self.friendSimpleInfoList:
            chatListItem = {}
            chatListItem['friendInfo'] = item
            chatList = ChatList(self.spider, item)
            chatListItem['chatList'] = chatList.work()

            self.allChatLists.append(chatListItem)
        print ('Set all chatlists content successfully')

    def saveAllChatListsContent(self):
        with open(self.chatfilePath, 'wb+') as f:
            for item in self.allChatLists:
                friendInfo = item['friendInfo']
                chatList = item['chatList']

                line = '*** : ' + friendInfo['name'] + '(' + friendInfo['uid'] + ')' + '*****************' + '\n\n'
                line += Config.GAP
                f.write(line.encode('utf-8'))
                for itemChat in chatList:
                    lineChat  = '*** ' + itemChat['time'] + ' ***' + '\n\n'
                    lineChat += '*** ' + itemChat['fromName'] + '(' + itemChat['fromId'] + ')' + ': ' + '\n\n'
                    lineChat += itemChat['content'] + '\n\n'
                    f.write(lineChat.encode('utf-8'))
            print ('Save all chatLists content successfully')


    def work(self):
        print ('111111111111111111111')	
        i = 0
        showNumEachPage = 50  #当前页显示多少个好友信息
        while True:
            st = i*showNumEachPage  #从st的下一个开始显示，比如st是100，则从101号好友开始显示
            lt = showNumEachPage  #页面显示好友信息数量，比如st是100，it是20，则从101开始显示到121号好友，如果总数不足则显示到最后
            result = self.setFriendSimpleInfoContent(self.spider.getContent(self.getFriendListForChatURL(st, lt)))
            i += 1
            if i == 20:
                break
            if result == False:
                break
        print ('2222222222222222222222222')	
        self.setAllChatListsContent()
        print ('3333333333333333333333333')	
        self.saveAllChatListsContent()	

