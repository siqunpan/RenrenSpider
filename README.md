# RenrenSpider

注意：
	由于本文本是在Windows上编辑，因此使用的是CRLF文本换行的方式。
    CRLF, LF 是用来表示文本换行的方式。CR(Carriage Return) 代表回车，对应字符 '\r'；LF(Line Feed) 代表换行，对应字符 '\n'。由于历史原因，不同的操作系统文本使用的换行符各不相同。主流的操作系统一般使用CRLF或者LF作为其文本的换行符。其中，Windows 系统使用的是 CRLF, Unix系统(包括Linux, MacOS近些年的版本) 使用的是LF。

这个project主要用来从 www.renren.com 上爬取并下载如下信息:
	1. 相册照片及评论album and photo
	2. 日志及评论blog
	3. 状态及评论status
	4. 留言板功能gossip(旧版人人，新版保留了)
	5. 聊天功能chat(新版人人)
	6. 自己以及所有好友的信息，先存储到mysql数据库中，再存储到本地

通用：
	1 我是通过Chrome的开发者工具的element选项查看的网页html代码，以及通过network选项进行抓包的，通过查看人人网html里charset属性得知人人网网页编码格式是utf-8
	2 在使用json.load()获得python的dictionary格式数据之后，知道dictionary中的key值信息有两种方式：
        2.1 通过print()函数打印出服务器返回的content
        2.2 如果服务器返回的数据是json格式，则将google开发者工具中network，中捕获的数据中的request url输入到网址栏，就可以看到范返回数据。
        	但是如果服务器返回的是数据是html格式字，json数据是通过beautifulsoup对象查询获得，这种情况下这个第二种方法就不适用，
	        只能适用打印信息的方法


Config.py:
	全局配置参数，包括路径，所需url等

PrivateConfig.py:(未传到github上)
	个人信息配置参数文件，内容如下：
		# -*- coding: utf-8 -*-

		Email = 'youremail'
		Password = 'yourpassword'
		OwnerID = 'yourid'

CommonFunction.py:
	一些通用的函数写在这里

登陆过程：
    客户端通过URL链接服务器请求信息的时候，服务器会发来cookie信息，之后客户端只有把cookie存储到本地，之后每次请求都会将cookie
    包含到请求信息request中，之后服务器能够识别该客户端，之后就可以进行通信了。
    因此我们要通过模拟人人网登陆获取第一个本地cookie文件，之后就可以使用该cookie了，注意该cookie有expire属性，即过期时间，因此
    隔一天左右会要求重新获取。
    Spider.py: 
        login(self):
    		1 先读取本地cookie进行验证，验证通过则直接进入人人网主页，
    	否则没有cookie或者cookie验证不通过则重新获取验证码图片输入验证码来获取cookie，该重新获取的请求request为post类型，通过
    	抓包观察Form Data结构得到需要提供的数据，即用户名，密码以及验证图片中的验证码
    		2 这里注意在登陆的时候要在headers中加上User-Agent，否则会报错

        getRawContent(self, url, data = None):
        	用来用url请求服务器数据，传递data参数说明是post类型，否则为get类型的请求request，使用response.read()可以读取html

不同功能的数据抓取以及下载大概流程：
	构造URL -> 向服务器发送请求request (geth或者post类型) -> 服务器返回数据 -> 解析数据 ->保存数据到本地

评论：
	Comment.py:
		1 通过分析人人网不同功能的评论的URL可知，其模式相同，只是通过传递不同类型参数判定是不同功能下的评论
		2 流程：
			构造URL->向服务器发送get类型请求request -> 服务器返回数据 -> 返回数据为满足json格式的字符串，因此直接通过json.loads()
			转化为python中的dictionary类型(不需要使用CommonFunction.generateJson()来将不满足json的部分转化为json格式)，并将中文的unicode编码转化为中文 -> 保存数据，并存储到本地
		3 setContent(self, content)函数中，有时候会出现找不到'comments'这个key，解决办法是打印一下服务器返回的数据就好了。。。

相册和照片部分：
	AlbumManager.py:
		1 服务器返回的是html格式数据，不是json格式，需要查询获得html中需要的json数据， 因此要使用BeautifulSoup()从HTML或XML文件中提取所需的json数据。beautifulsoup自动将输入文档转换为Unicode编码，输出文档转换为utf-8编码。得到一个BeautifulSoup的对象, 
		3 保存获取的相册列表数据，并开始处理每一个相册
	Album.py:
		1 流程跟AlbumManager.py差不多，只是改为获取该相册中的照片列表，并增加了一个捕捉并保存相册评论到本地的部分
	Photos.py:
		1 构造URL获取该照片的详细信息，
        






