# -*- coding: utf-8 -*-

'''
    #为了防止敏感信息被上传到github，因此个人信息改为写到ignorelist中的PrivateConfig.py
    Email = 'EnterYourOwn'
    Password = 'EnterYourOwn'
    OwnerID = 'EnterYourOwn'

'''

CookieFile = 'cookie.txt'
GossipFile = 'gossip.markdown'
ChatFile = 'chat.markdown'
DBName = 'renren'  #数据库名字
DBTableName = 'people'  #存储所有好友信息的数据库表
DBFile = 'people.markdown'  #存储所有好友信息的本地文件
PublicPageDBTableName = 'publicPage'    #存储所有公共主页信息的数据库表
PublicPageDBFile = 'publicPage.markdown'  #存储所有公共主页信息的本地文件

#这些是建立数据库连接的时候的设置，其中注意密码passwd
DBConnectInfo = {
                   'host':'localhost',
                   'user':'root',
                   'passwd':'root',
                   #'db': 'renren',  #在RepoMysql.py中通过useDbSql指令设置也可以，
                                         #但是好像只在这里设置，不使用useDbSql函数就不会生效，所以最后就不在这里设置了
                   'charset':'utf8'  #在RepoMysql.py中通过set_character_set指令设置也可以，
                                         #但是pymysql会报错没有set_character_set这个指令，所以就在这里设置了
                }

DATAPATH = 'data'
BLOGPATH = 'blogs'
ALBUMLISTPATH = 'albumlist'

'''
***********************
看URL返回内容从而确定可以通过那些标签获取所需数据的方法：
    1 直接将URL输入进浏览器看返回页面，比如http://friend.renren.com/groupsdata
    2 一些URL是程序提供数据组合而成，则通过在程序中print()函数打印open()这个url之后的返回内容获得
***********************
'''

'''
下面两个登陆的URL都适用：F12开启google开发者工具(勾选 preserve log选项)
  1 在人人网登陆界面，在Elements页面能找到http://www.renren.com/PLogin.do这个链接
  2 人人网登陆之后进入首页，在Network页面可以找到login？开头的Method為post方法的条目，里面可以
    得到http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2016202210414这个链接
    并且在Form Data表单数据栏可以看到需要提供的数据
'''
LOGINURL = r'http://www.renren.com/PLogin.do'
#LOGINURL = 'http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2016202210414'

#验证码的URL可以通过打开人人网登陆界面，F12开启google开发者工具，在Network页面中一个getcode开头的条目中的Request URL找到的
ICODEURL = r'http://icode.renren.com/getcode.do?t=login&rnd=Math.random()'

#评论的URL可以通过打开人人网任一个相册，F12开启google开发者工具，在Network页面中一个xoa开头的条目中的Request URL找到的
COMMENTURL = r'http://comment.renren.com/comment/xoa2'

#相册列表的URL可以通过进入相册列表页面后，在google开发者工具的Network页面中的v7开头的条目中的request URL找到
ALBUMLISTURL = r'http://photo.renren.com/photo/%s/albumlist/v7'

#相册的URL可以通过进入一个相册后，在google开发者工具的Network页面中的v7开头的条目中的request URL找到
ALBUMURL = r'http://photo.renren.com/photo/%s/album-%s/v7'

#状态的URL获得：进入状态页面，在google开发者工具的Network页面中的GetSomesomeDoingList开头的条目中的request URL找到
STATUSURL = r'http://status.renren.com/GetSomeomeDoingList.do'

'''
每张照片的URL的获得比较特殊，因为现在在人人网相册中点击其中的一张照片，不会弹出新的连接，而是在已有连接上弹出该照片
这样就导致我们无法通过Chrome的开发者工具的network页面中通过抓包获得该照片的URL。
正确的方法是，在该相册页面中，在Chrome的开发者工具的element页面下，从html代码中找到任意一张照片的部分，
注意这里指的不是header标签部分，而是body中的部分。在body中每一张照片都有一个叫'photo-box'的标签，在这个标签下就可以
得到每张照片的URL了，从而也知道了照片的URL的格式，然后点击任意一个URL即可打开属于该照片的页面，注意勾选preserve log选项，
在这个新页面中，就可以在network中的叫v7的条目中找到对应URL了，其实这个URL就是之前点击的那个
'''
PHOTOSURL = r'http://photo.renren.com/photo/%s/photo-%s/v7'

'''
点击照片弹出的URL
'''
POPUPPHOTOURL = r'http://photo.renren.com/photo/%s/album-%s/v7#photo/%s/%s'

#日志列表的URL获得：进入日志主页面，此时在google开发者工具的Network页面中是找不到这个url的，要想获得需要这个url，需要
#点击日志主页最下面的翻页按钮，或者直接点击另外一页，此时Network就回抓到名字是blog?categoryId开头的条目的包，里面的
#Request Url就是这个我们需要的URL。
#这种获取方式好奇怪，必须翻页或者其他页面数字才行。。。
BLOGLISTURL = r'http://blog.renren.com/blog/%s/blogs?'

#某一个日志的URL获得：进入该日志页面，在google开发者工具的Network页面中以该日志编号为名字的条目中的request URL找到
BLOGURL = r'http://blog.renren.com/blog/%s/%s?bfrom=01020110200'
#BLOGURL = r'http://blog.renren.com/blog/%s/%s    #去掉'?bfrom=01020110200''这段也没问题

#留言板URL获得(现在留言板已经换为聊天功能，但是留言板仍然保留)：因为已经不再用，因此，在renren网个人主页，通过在google
#开发者工具的Element页面中获得这个URL
#或者在人人网个人主页会有提示“留言功能已全面升级为聊天，查看历史留言记录”，点击可以进入留言板，此时在network中是捕捉不到
#这个URL的包的，需要随便翻到另外一页，然后再network中可以找到叫ajaxgossiplist.do的条目，这个Request URL就是我们需要的
#注意这个URL请求方法为post，不是get
GOSSIPURL = r'http://gossip.renren.com/ajaxgossiplist.do'

#聊天URL获得：在人人网主界面的聊天区域，打开任一人的聊天窗口在network中都会抓到名字以getChatList?开头的数据包
CHATURL = r'http://webpager.renren.com/api/getChatList'

#个人信息页面，在进入该页面之后，刷新一下，然后在network中可以找到叫profile?v=info_timeline的条目，
#这个Request URL就是我们需要的
PERSONALINFOURL = r'http://www.renren.com/%s/profile?v=info_timeline'

#所有好友信息URL：打开好友页面，在google开发者工具的network页面中groupsdata数据包里的Request URL
#注意还有一个叫managefriends的数据包，这个不是我们要的，因为返回页面数据里没有所有好友的全部信息，只有部分简略信息
FRIENDLISTURL = r'http://friend.renren.com/groupsdata'

#新版人人网好友URL：获取方法为点击人人网主页右上角好友按钮，然后下拉好友菜单就能在network中捕捉到了
#这个URL在程序里只用来获得每个好友的聊天信息，而不是获得详细好友信息
FRIENDLISTURLNEW = r'http://webpager.renren.com/api/getFriendsInfo'

#部分人人网公共主页的URL，用于获取好友信息时遇到公共主页的情况
PUBLICPAGEURL = r'http://page.renren.com/%s?v=info_timeline'

#部分人人网公共主页信息的URL，用于获取好友信息时遇到公共主页的情况
PUBLICPAGEINFOURL = r'http://page.renren.com/%s/info'

#在短时间内连续查看了100个人的页面之后会弹出验证页面，可能是为了防止爬虫
#获得方式：在打开一个url之后，对返回的内容对象调用geturl()方法获得返回的url，然后对比这两url，如果不一样则说明
#返回的url可能是输入验证码页面，此时打印出这个url就得到这个url了，如果不是输入验证码页面，则说明是异常
VALIDATEURL = r'http://www.renren.com/validateuser.do'

# FailCode via "login-v6.js"
FAILCODE = {
            '-1': '登录成功',
            '0': '登录系统错误，请稍后尝试',
            '1': '您的用户名和密码不匹配',
            '2': '您的用户名和密码不匹配',
            '4': '您的用户名和密码不匹配',
            '8': '请输入帐号，密码',
            '16': '您的账号已停止使用',
            '32': '帐号未激活，请激活帐号',
            '64': '您的帐号需要解锁才能登录',
            '128': '您的用户名和密码不匹配',
            '512': '请您输入验证码',
            '4096': '登录系统错误，稍后尝试',
}

GAP = '\n**********************\n'