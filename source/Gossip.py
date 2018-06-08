# -*- coding: utf-8 -*-

import urllib
import json
import Config

class Gossip:

    def __init__(self, spider, userID, ownerID):
        self.url = Config.GOSSIPURL
        self.spider = spider
        self.userID = userID
        self.ownerID = ownerID
        self.gossipCount = 0
        self.gossipContent = []

    def setGossipCount(self, content):
        dictInfo = json.loads(content)
        #print ('********dictInfo for obtaining quantity of gossips: ', dictInfo)
        #'gossipCount'这个标签是通过打印出来返回数据观察得到
        self.gossipCount = dictInfo['gossipCount']

    def getGossipData(self, pageNo = 0):
    	data = {
                'guest': self.userID,
                'curpage': -1,
                'destpage': 0,
                'page': pageNo,
                'id': self.ownerID,
                'resource': 'undefined',
                'search': 0,
                'boundary': 0,
                'gossipCount': self.gossipCount
    	        }
    	return urllib.parse.urlencode(data)

    def setContent(self, content):
        dictInfo = json.loads(content)
        for item in dictInfo['array']:
            info = {}
            info['time'] = item['time']
            info['guestId'] = item['guestId']
            info['guestName'] = item['guestName']
            info['filterdBody'] = item['filterdBody']
            info['id'] = item['id']
            if item['gift'] == 'true':
                info['isGift'] = True
            else:
                info['isGift'] = False
            self.gossipContent.append(info)
    
    def saveContent(self):
        with open(Config.DATAPATH + '/' + self.ownerID + '/gossip.markdown', 'wb') as f:
            str1 = 'Quantity of gossips: ' + str(self.gossipCount) + '\n'
            f.write(str1.encode('utf-8'))
            f.write(Config.GAP.encode('utf-8'))
            for item in self.gossipContent:
                line = 'id: ' + item['id'] + '\n\n'
                line += 'time: ' + item['time'] + '\n\n'
                line += 'guestId: ' + item['guestId'] + '\n\n'
                line += 'guestName: ' + item['guestName'] + '\n\n'
                line += 'isGift: ' + str(item['isGift']) + '\n\n'
                line += 'filterdBody: ' + item['filterdBody'] + '\n'
                line += Config.GAP
                f.write(line.encode('utf-8'))
        print ('save gossip complete')

    def work(self):
        #任何一个留言页面的返回数据中都有gossipCount这个留言总数的数据，因此我们这里取第一页的返回数据就可以了
        self.setGossipCount(self.spider.getContent(self.url, self.getGossipData(0).encode('utf-8')))
        i = 0
        gossipMaxNumEachPage = 20  #每一页的留言最大数量
        for i in range(0, self.gossipCount//gossipMaxNumEachPage + 1):
            self.setContent(self.spider.getContent(self.url, self.getGossipData(i).encode('utf-8')))
        self.saveContent() 