# -*- coding: utf-8 -*-

'''
    This project works for spidering and download info from www.renren.com include:
    1. personal info
    2. photos
    3. blogs
    4. status
    5. friends info
    6. comments
    7. gossip (old renren version)
    8. chat (new renren version)
    9. save your own and all your friends personal info into a database(mysql)
'''

from Spider import RenrenSpider
from AlbumManager import AlbumManager
from Status import Status
from BlogManager import BlogManager
from Gossip import Gossip
from RepoMysql import RepoMysql

import datetime
import CommonFunction
import Config

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

    CreatePaths(userID)  #userID of url opened
    CreatePaths(ownerID = Config.OwnerID)  #userID of your own
    
    print ('userID and ownerID: ', userID, ', ', Config.OwnerID)

    #albumManager = AlbumManager(baobao, userID, Config.OwnerID)
    #albumManager.work()

    #blogManager = BlogManager(baobao, userID, Config.OwnerID)
    #blogManager.work()

    #status = Status(baobao, userID, Config.OwnerID)
    #status.work()

    #gossip = Gossip(baobao, userID, Config.OwnerID)
    #gossip.work()

    repo = RepoMysql(baobao, userID)
    repo.work()

    endDatetime = datetime.datetime.now()
    print('All info of renren.com have been downloaded with time: ', endDatetime - beginDateTime)

Main()


