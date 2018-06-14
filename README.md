# RenrenSpider

注意：
	由于本文本是在Windows上编辑，因此使用的是CRLF文本换行的方式。
    CRLF, LF 是用来表示文本换行的方式。CR(Carriage Return) 代表回车，对应字符 '\r'；LF(Line Feed) 代表换行，
    对应字符 '\n'。由于历史原因，不同的操作系统文本使用的换行符各不相同。主流的操作系统一般使用CRLF或者LF作为其文本
    的换行符。其中，Windows 系统使用的是 CRLF, Unix系统(包括Linux, MacOS近些年的版本) 使用的是LF。

这个project主要用来从 www.renren.com 上爬取并下载如下信息:
	1. 相册照片及评论album and photo
	2. 日志及评论blog
	3. 状态及评论status
	4. 留言板功能gossip(旧版人人，新版保留了)
	5. 聊天功能chat(新版人人)
	6. 自己以及所有好友的信息，先存储到mysql数据库中，再存储到本地

通用：
	1 我是通过Chrome的开发者工具的element选项查看的网页html代码，以及通过network选项进行抓包的，通过查看人人网html里
		charset属性得知人人网网页编码格式是utf-8
	2 爬取数据的一些工作重点：
		2.1 如何模拟登陆
		2.2 如何获得相应的URL并构造出需要的URL，不同功能模块URL的获取方式并不一样，有些直接就能抓包得到，有些需要一些
			点击操作才能抓包得到，有些需要从html数据中得到。之后是如何根据这些得到的URL例子，观察规律构造自己的URL，
			比如评论comment，留言板等的url。
			每个功能URL获得的方式我都在Config.py中的注释中写明了
		2.3 服务器返回的数据有html格式的(用beautifulsoup获取所需数据)，有json格式的，需要不同方式处理，
			以及要分析返回数据，已获得自己需要的
		2.4 一些数据规模较大，比如照片数据，因此需要进行优化，不用每次运行都重新从远程服务器下载到本地
	3 在使用json.load()获得python的dictionary格式数据之后，知道dictionary中的key值信息有两种方式：
        2.1 通过print()函数打印出服务器返回的content
        2.2 如果服务器返回的数据是json格式，则将google开发者工具中network，中捕获的数据中的request 
        	url输入到网址栏，就可以看到范返回数据。
        	但是如果服务器返回的是数据是html格式字，json数据是通过beautifulsoup对象查询获得，这种情况下这个第二种方法
        	就不适用，只能适用打印信息的方法


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
    			否则没有cookie或者cookie验证不通过则重新获取验证码图片输入验证码来获取cookie，该重新获取的请求request为post方法，通过抓包观察Form Data结构得到需要提供的数据，即用户名，密码以及验证图片中的验证码
    		2 这里注意在登陆的时候要在headers中加上User-Agent，否则会报错

        	3 getRawContent(self, url, data = None):
        		用来用url请求服务器数据，传递data参数说明是请求为post方法，否则为get方法的请求request，使用response.read()可以读取html

不同功能的数据抓取以及下载大概流程：
	构造URL -> 向服务器发送请求request (get或者post方法) -> 服务器返回数据 -> 解析数据 ->保存数据到本地

所有功能涉及的评论：
	Comment.py:
		1 通过分析人人网不同功能的评论的URL可知，其模式相同，只是通过传递不同类型参数判定是不同功能下的评论
		2 流程：
			构造URL->向服务器发送get类型请求request -> 服务器返回数据 -> 返回数据为满足json格式的字符串，因此直接通过json.loads()
			转化为python中的dictionary类型(不需要使用CommonFunction.generateJson()来将不满足json的部分转化为json格式)，并将中文的unicode编码转化为中文 -> 保存数据，并存储到本地
		3 setContent(self, content)
			函数中，有时候会出现找不到'comments'这个key，解决办法是打印一下服务器返回的数据就好了。。。
		4 通过服务器返回数据得知是否所有评论都处理完，如果没有构造新的URL向服务器发送请求

相册和照片：
	AlbumManager.py:
		1 服务器返回的是html格式数据，不是json格式，需要查询获得html中需要的json数据， 因此要使用BeautifulSoup()从HTML或XML文件中提取所需的json数据。beautifulsoup自动将输入文档转换为Unicode编码，输出文档转换为utf-8编码。得到一个BeautifulSoup的对象, 
		3 保存获取的相册列表数据，并开始处理每一个相册
	Album.py:
		1 流程跟AlbumManager.py差不多，只是改为获取该相册中的照片列表，并增加了一个捕捉并保存相册评论到本地的部分
	Photos.py:
		1 构造URL获取该照片的详细信息，跟AlbumManager.py相同，通过beautifulsoup从返回的html中取得数据，修整以满足json格式之后转换为
	python的dictionary格式，之后获得照片详细信息
		2 保存照片图片到本地：建立一个openner，之后通过照片url将照片从远程数据下载到本地
		3 保存照片评论到本地：就是将之前保存的照片详细信息中的评论信息写入到本地文件中

日志：
	BlogManager.py:
		1 大致流程相同，构造url，向服务器发送请求，方法为get，服务器返回数据，解析数据，保存数据到本地
		2 先获得日志列表的信息，包含所有日志的基本信息，服务器返回的直接就是json数据，因此直接json.loads()成dictionary格式进行
			处理就好
		3 通过上面保存的日志列表信息处理每一篇日志
	Blog.py:
		1 通过上面保存的日志列表信息获取每一个日志数据，注意服务器返回的日志数据是html格式的，因此先用beautifulsoup来从返回数据中找到日志正文数据，但是这个数据仍然是html，因此需要使用正则表达式将标签替换成换行符，以方便阅读，否则所有正文全部在一行。注意还要处理该日志的评论数据

发表的状态：
	Status.py:
		1 通用方式，就是构造URL，方法为get -> 服务器返回数据直接就是json格式，转化为dictionary，解析数据 -> 保存数据到本地
		2 使用一个计数器构造URL，当服务器返回数据中没有所需数据时，说明处理完毕

留言板(旧版人人，新版保留了):
	Gossip.py:
		1 通用方式，就是构造URL，方法为post -> 服务器返回数据直接就是json格式，转化为dictionary，解析数据 -> 保存数据到本地

聊天(新版人人):
	ChatManager.py:
		1 观察同一个好友聊天窗口的URL观察得知，要构造一个聊天URL需要获取该好友的id，所以我们需要获取所有好友的id
		2 获取所有好友id的方法：通过聊天窗口的好友选项获得所有好友的基本信息列表，这里没有从人人网的好友页面获取，
		因为我们只需要好友的id和name(name其实也不需要)就行，不需要其余信息
		3 通过好友id构造和每一个好友的聊天url，分析返回数据获得聊天列表，为空则没有聊天记录
		4 注意构造url的方法，需要一些计数器来构造
		5 其余就是通用请求流程，这里所有请求都是get方法
	ChatList.py:
		1 处理和一个好友的聊天数据

自己以及所有好友信息:
	RepoMysql.py:
		1 建立python和MySQL数据库的连接对象connect，以及数据库的交互对象cursor
		2 之后的流程：建立数据库 -> 发送请求获得自己以及所有好友信息 -> 将数据插入数据库 -> 将数据库数据保存到本地
		3 select * from people into outfile 只能输出到mysql指定的位置，
        	我尝试了网上的更改secure_file_priv的方法，发现还是不能输出到我的工程目录下，
        	我采用的方法就是在python中获得secure_file_priv路径，然后找到输出的文件，
        	最后移动该文件到工程指定的目录下
	FriendList.py:
		1 获得所有好友的基本信息，详细信息通过PersonalInfo.py获得
		2 URL请求方法为get，注意服务器返回数据不满足json格式，因此需要先手动找到"data"属性的数据，这部分数据基本满足
		json格式要求，但是还需要进行格式修正再进行处理

	PersonalInfo.py:
		1 URL请求方法为get, 服务器返回数据为html格式，因此还是需要使用beautifulsoup进行转换，之后再找到需要的部分数据，
			其基本满足json格式，修正不满足的然后通过json.loads()转化为python的dictionary,最后就可以尽心处理了
		2 注意由于要想服务器请求包括自己在内的所有好友的信息，人人网在访问100个好友的时候回要求输入验证码，程序里的处理
			就是当服务器返回数据中附带的Request url和发送请求的url不同的时候，说明服务器返回的是输入验证码的页面(如果
			经过判断不是这个页面，如果该页面也不是公共主页，则说明出现了位置错误，返回了未知页面)

	PublicPage.py:
	    1 处理好友是公共主页的情况，和处理好友方法类似

        






