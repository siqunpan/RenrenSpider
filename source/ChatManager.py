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
            info['uid'] = str(item['uid'])
            info['name'] = item['name']
            self.friendSimpleInfoList.append(info)
        if len(dictInfo['data']['items']) > 0:
            return True
        else:
            return False

    def setAllChatListsContent(self):
        for item in self.friendSimpleInfoList:
            chatList = ChatList(self.spider, item)
            chatListInfo = chatList.work()
            if len(chatListInfo) > 0:
                chatListItem = {}
                chatListItem['friendInfo'] = item
                chatListItem['chatList'] = chatListInfo
                self.allChatLists.append(chatListItem)
        print ('Set all chatlists content successfully')

    def saveAllChatListsContent(self):
        with open(self.chatfilePath, 'wb+') as f:
            for item in self.allChatLists:
                friendInfo = item['friendInfo']
                chatList = item['chatList']

                line  = '------------------------ '
                line += friendInfo['name'] + '(' + friendInfo['uid'] + ')'
                line += ' ------------------------' + '\n\n'
                f.write(line.encode('utf-8'))

                for itemChat in chatList:
                    lineChat  = '--- ' + itemChat['time'] + ' ---' + '\n\n'
                    lineChat += itemChat['fromName'] + '(' + itemChat['fromId'] + ')' + ': ' + '\n\n'
                    lineChat += '    ' + itemChat['content'] + '\n\n'
                    f.write(lineChat.encode('utf-8'))

            print ('Save all chatLists content successfully')


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
        self.setAllChatListsContent()  #读取和所有好友的聊天信息，并存储到列表中
        self.saveAllChatListsContent()	#将聊天信息保存到本地

