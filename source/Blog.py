# -*- coding: utf-8 -*-

import urllib
import json
import Config
import re

from bs4.element import NavigableString
from bs4 import BeautifulSoup
from Comment import Comment

class Blog:

    def __init__(self, spider, userID, ownerID, blogID, filename, summary):
        self.url = Config.BLOGURL % (ownerID,blogID)
        self.spider = spider
        self.userID = userID
        self.ownerID = ownerID
        self.blogID = blogID
        self.filename = filename
        self.summary = summary

    def saveBlog(self):
        #获取html中所需的内容，可以通过Chrome开发者工具的element选项在人人网该页面查看
        self.content = self.spider.getContent(self.url)
        soup = BeautifulSoup(self.content)
        blogContent = soup.find('div', id = 'blogContent', class_ = 'blogDetail-content')
        
        #将标签换位换行符，方便阅读
        pattern = r'<p>|<br>|</p>|<br/>'  #将<p>,<br>,</p>和<br/>四个标签换为换行符\n
        blogContent = re.sub(pattern, r'\n', blogContent.decode())

        with open(self.filename, 'wb+') as f:
            line  = u'*** 日志标题: ***' + self.summary['title'] + '\n\n'
            line += u'*** 创建时间: ***' + self.summary['createTime'] + '\n\n'
            line += u'*** 所属分类: ***' + self.summary['category'] + '\n\n'
            line += Config.GAP
            f.write(line.encode('utf-8'))
            f.write(blogContent.encode('utf-8'))
            if int(self.summary['commentCount']):
                f.write(Config.GAP.encode('utf-8'))
                f.write((u'*** 评论: ***\n\n').encode('utf-8'))
                comments = Comment(self.spider, self.userID, self.blogID, 'blog', self.ownerID)
                f.write(comments.work())
        print (self.filename + ' saves successfully')

    def work(self):
        self.saveBlog()
