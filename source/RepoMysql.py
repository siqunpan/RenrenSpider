# -*- coding: utf-8 -*-

import Config
import datetime
import CommonFunction
import re
import shutil

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
createDbSql = 'create database if not exists %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci'

useDbSql = 'use %s'

createSql = 'create table %s(\
                id char(9) not null,\
                name varchar(15),\
                relation char(6),\
                gender char(1),\
                birth varchar(20),\
                hometown varchar(20),\
                belong varchar(40),\
                firstGroup varchar(20),\
                secondGroup varchar(20),\
                edu varchar(200),\
                comf varchar(4),\
                primary key (id))'

insertSql = 'insert into %s \
            (id,name,relation,gender,birth,hometown,belong,firstGroup,secondGroup,edu,comf) values \
            ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'

outputSql = 'select * from %s into outfile "%s"'

showOutputFilePathSql = 'show variables like \'secure_file_priv\''

dropDatabaseSql = 'drop database %s'

class RepoMysql:

    def __init__(self, spider, userID, ownerID):
        #建立数据库连接对象
        self.connect = pymysql.connect(**Config.DBConnectInfo)
        #建立数据库交互对象
        self.cursor = self.connect.cursor()
        self.spider = spider
        self.userID = userID
        self.ownerID = ownerID
        self.peopleList = []

    def __del__(self):
        #先关闭数据库交互对象cursor，再关闭数据库连接对象connect
        self.cursor.close()
        self.connect.close() 

    def dropDB(self):
        try:
            #删除数据库表
            self.cursor.execute(dropDatabaseSql % Config.DBName)
            #提交数据库操作
            self.connect.commit()

        except Exception as e:
            print (e)
            #回滚当前事务
            self.connect.rollback() 
        else:
            print('Drop database successfully')   

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
            self.cursor.execute(useDbSql % Config.DBName)
            #self.connect.set_character_set('utf8')

            #创建数据库表
            self.cursor.execute(createSql % Config.DBTableName)
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
                paramTup = (Config.DBTableName,)  #建立单个元素的tuple，使用逗号
                paramTup = paramTup + item
                self.cursor.execute(insertSql % paramTup)
        except Exception as e:
            print (e)
            #回滚当前事务
            self.connect.rollback()
        else:
            print ('Insert database successfully')

    '''
        select * from people into outfile 只能输出到mysql指定的位置，
        我尝试了网上的更改secure_file_priv的方法，发现还是不能输出到我的工程目录下，
        我采用的方法就是在python中获得secure_file_priv路径，然后找到输出的文件，
        最后移动该文件到工程指定的目录下
    '''
    def outputDB(self):
        try:
            #获取MySQL规定默认输出文件路径，由于结果集是是tuple,所以可以像数组一样使用结果集获取数据
            setCount = self.cursor.execute(showOutputFilePathSql)
            rows = self.cursor.fetchall()
            outputFilePath = rows[0][1]

            #将'\'换为'/'，以满足python路径格式
            pattern = r'\\'
            outputFilePath = re.sub(pattern, r'/', outputFilePath)
            outputFilePath = outputFilePath + Config.DBName + '/' + Config.DBFile

            CommonFunction.RemoveFile(outputFilePath)  #如果该文件事先已存在则先删除，否则会报错

            #先输出查询数据到MySQL指定路径
            self.cursor.execute(outputSql % (Config.DBTableName, Config.DBFile))
            self.connect.commit()

            destPath = Config.DATAPATH + '/' + self.ownerID + '/' + Config.DBFile
            #最后将指定路径下的输出文件移动到工程目录下
            shutil.move(outputFilePath, destPath)

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
        endDatetime = datetime.datetime.now()
        print ('Collect all people info successfully, time: ', endDatetime - beginDatetime)

    def work(self):
        self.dropDB()   #即使使用了 create database if not exists，但是仍然会报错 database ‘renren’ already exists
                            #的错误，所以先删除数据库再建立
        self.createDB()  #建立数据库以及用表
        self.collectInfo()  #收集自己以及所有好友信息      
        self.insertDB()  #将收集到的信息写入数据库
        self.outputDB()   #输出数据库信息到指定文件