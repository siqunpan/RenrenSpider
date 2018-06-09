# -*- coding: utf-8 -*-

import Config
import datetime

#MySQLdb和pymysql都是数据库的操作模块，其中pymysql支持python3.x， 而MySQLdb不支持3.x版本
#import MySQLdb 
import pymysql
pymysql.install_as_MySQLdb()

from PersonalInfo import PersonalInfo
from FriendList import FriendList

#所需数据库命令
'''
    cursors.py:170: Warning: (3719, "'utf8' is currently an alias for the character set UTF8MB3, 
      which will be replaced by UTF8MB4 in a future release. Please consider using UTF8MB4 in order 
    to be unambiguous.")
'''
createDbSql = 'create database if not exists %s DEFAULT CHARACTER SET UTF8MB4 COLLATE utf8mb4_general_ci'
useDbSql = 'use %s'
createSql = 'create table people(\
                id char(9) not null,\
                name varchar(15),\
                relation char(6),\
                gender char(1),\
                birth varchar(20),\
                hometown varchar(20),\
                belong varchar(20),\
                firstGroup varchar(20),\
                edu varchar(200),\
                comf varchar(4),\
                primary key (id))'
insertSql = 'insert into people \
            (id,name,relation,gender,birth,hometown,belong,firstGroup,edu,comf) values \
            ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
outputSql = 'select * from people into outfile "%s"' % Config.DBFile

class RepoMysql:

    def __init__(self, spider, userID):
        #建立数据库连接对象
        self.connect = pymysql.connect(**Config.DBConnectInfo)
        #建立数据库交互对象
        self.cursor = self.connect.cursor()
        self.spider = spider
        self.userID = userID
        self.peopleList = []

    def __del__(self):
        #先关闭数据库交互对象cursor，再关闭数据库连接对象connect
        self.cursor.close()
        self.connect.close() 

    def createDB(self):
        try:
            #建立数据库
            self.cursor.execute(createDbSql % Config.DBName)

            '''
                下面useDbSql和set_character_set要么在这里设置，要么在config的dbConnectInfo中添加
                注意：由于报错'Connection' object has no attribute 'set_character_set'
                     因此不能用下面的方式了，必须要在config的dbConnectInfo中添加
            '''
            #通告MySQL把Config.DBName数据库作为默认（当前）数据库使用，用于后续语句
            #self.cursor.execute(useDbSql % Config.DBName)
            #self.connect.set_character_set('UTF8MB4')

            #创建数据库表
            self.cursor.execute(createSql)
            #提交数据库操作
            self.connect.commit()

        except Exception as e:
            print (e)
            #回滚当前事务
            self.connect.rollback() 
        else:
            print('Create database successfully')

    def insertDB(self):
        try:
            for item in self.peopleList:
                self.cursor.execute(insertSql % item)
        except Exception as e:
            print (e)
            #回滚当前事务
            self.connect.rollback()
        else:
            print ('Insert database successfully')

    def outputDB(self):
        try:
            self.cursor.execute(outputSql)
            self.connect.commit()
        except Exception as e:
            print (e)
            #回滚当前事务
            self.connect.rollback()
        else:
            print ('Output database successfully')

    def collectInfo(self):
        myself = PersonalInfo(self.spider, self.userID, self.userID)
        self.peopleList.append(myself.work())

        friendList = FriendList(self.spider)
        friends = friendList.work()
        i = 1
        count = len(friends)
        beginDatetime = datetime.datetime.now()
        print ('Begin to collect all people info, time: ', beginDatetime)
        for item in friends:
            friend = PersonalInfo(self.spider, self.userID, item['fid'], item)
            self.peopleList.append(friend.work())
            if i % 100 == 0:
                print ('Already collect %d/%d people info, time: ' % (i, count), datetime.datetime.now())
            i += 1

            if i == 10:
                break

        endDatetime = datetime.datetime.now()
        print ('Collect all people info successfully, time: ', endDatetime - beginDatetime)

    def work(self):
        print ('1111111111111111111111111111')
        self.createDB()  #建立数据库以及用表
        print ('2222222222222222222222222222')
        self.collectInfo()  #收集自己以及所有好友信息
        print ('3333333333333333333333333333')        
        self.insertDB()  #将收集到的信息写入数据库
        print ('4444444444444444444444444444')
        self.outputDB()   #输出数据库信息到指定文件