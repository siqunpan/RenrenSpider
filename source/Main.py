# -*- coding: utf-8 -*-

'''
    这个project主要用来从www.renren.com上爬取并下载如下信息:
    1. 相册照片及评论album and photo
    2. 日志及评论blog
    3. 状态及评论status
    4. 留言板功能gossip(旧版人人，新版保留了)，留言板(旧)和聊天(新)信息不一样
    5. 聊天功能chat(新版人人)，留言板(旧)和聊天(新)信息不一样
    6. 自己以及所有好友的信息，先存储到mysql数据库中，再存储到本地

    通用：
    1 我是通过Chrome的开发者工具的element选项查看的网页html代码，以及通过network选项进行抓包的，
        通过查看人人网html里charset属性得知人人网网页编码格式是utf-8
    2 在使用json.load()获得python的dictionary格式数据之后，知道dictionary中的key值信息有两种方式：
        2.1 通过print()函数打印出服务器返回的content
        2.2 如果服务器返回的数据是json格式，则将google开发者工具中network，中捕获的数据中的request url
            输入到网址栏，就可以看到范返回数据。
            但是如果服务器返回的是数据是html格式字，json数据是通过beautifulsoup对象查询获得，这种情况下
            这个第二种方法就不适用，只能适用打印信息的方法
'''

from Spider import RenrenSpider
from AlbumManager import AlbumManager
from Status import Status
from BlogManager import BlogManager
from Gossip import Gossip
from ChatManager import ChatManager
from RepoMysql import RepoMysql

import datetime
import CommonFunction
import Config
import PrivateConfig

def CreatePaths(ownerID):
    CommonFunction.CreatePath(Config.DATAPATH)
    CommonFunction.CreatePath(Config.DATAPATH + '/' + ownerID)
    CommonFunction.CreatePath(Config.DATAPATH + '/' + ownerID + '/' + Config.BLOGPATH)
    CommonFunction.CreatePath(Config.DATAPATH + '/' + ownerID + '/' + Config.ALBUMLISTPATH)

def Main():
    beginDateTime = datetime.datetime.now()

    baobao = RenrenSpider()
    baobao.login()
    userID = baobao.getUserID()

    CreatePaths(userID)  #在打开的URL中能使用的ID
    CreatePaths(ownerID = PrivateConfig.OwnerID)  #自己的ID
    
    print ('userID and ownerID: ', userID, ', ', PrivateConfig.OwnerID)

    #相册照片及评论album and photo
    albumManager = AlbumManager(baobao, userID, PrivateConfig.OwnerID)
    albumManager.work()

    # #日志及评论blog
    # blogManager = BlogManager(baobao, userID, PrivateConfig.OwnerID)
    # blogManager.work()

    # #状态及评论status
    # status = Status(baobao, userID, PrivateConfig.OwnerID)
    # status.work()

    # #留言板功能gossip(旧版人人，新版保留了)
    # gossip = Gossip(baobao, userID, PrivateConfig.OwnerID)
    # gossip.work()

    # #聊天功能chat(新版人人)
    # chatManager = ChatManager(baobao, userID, PrivateConfig.OwnerID)
    # chatManager.work()

    # #自己以及所有好友的信息，出现存储到mysql数据库中，再存储到本地
    # repo = RepoMysql(baobao, userID, PrivateConfig.OwnerID)
    # repo.work()

    endDatetime = datetime.datetime.now()
    print('All info of renren.com have been downloaded with time: ', endDatetime - beginDateTime)

Main()


