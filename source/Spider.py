# -*- coding: utf-8 -*-

import urllib
import urllib.request
import Config
import PrivateConfig
import http.cookiejar
import re
import CommonFunction


class RenrenSpider:
    
    '''
        This is the spider especially for www.renren.com
    '''
    #construction
    def __init__ (self):
        self.username = PrivateConfig.Email		#set username
        self.password = PrivateConfig.Password 	#set password
        self.cookie   = http.cookiejar.LWPCookieJar()	#declare cookiejar for storing cookie

        '''
            先读取本地cookie进行验证
            ignore_discard: save even cookies set to be discarded. 
            ignore_expires: save even cookies that have expiredThe file is overwritten if it already exists
        '''
        if CommonFunction.IsPathExist(PrivateConfig.CookieFile):
            self.cookie.load(PrivateConfig.CookieFile, ignore_discard=True, ignore_expires=True)

        #create cookie processor, build a opener and then set this opener the default opener 
        self.opener   = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
        urllib.request.install_opener(self.opener)

    #login function
    def login(self):
        '''
            Add the headers to avoid the error: urllib.error.HTTPError: HTTP Error 403: Forbidden
            That the website forbids spiders is the cause of the error, so we add headers in the request
            to disguise as browser access User-Agent.
            The User-Agent info of chrome browser can be obtained by input: about:version in the address bar

            Spider.py中还有另外一中设置header内容的写法
        '''
        #User-Agent
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        #create a request
        request = urllib.request.Request(url = 'http://www.renren.com', headers = headers)
        #open a url
        url = urllib.request.urlopen(request).geturl()
        print (url)
        if re.match('http://www.renren.com/[\d]{9}', url):
            #login succefully
            self.userID = url.split('/')[3]  #get userID
            print ('Login Successfully')
            return True
        else:
            #cookie not work, should relogin
            print ('Cookie file does not work anymore')

        #Form Data in the Headers of request URL
        data = {
                'email' : self.username,
                'password' : self.password,
                'origURL' : 'http://www.renren.com/home',
                'icode' : ''
        }
        isLogin = False
        failCodePattern = re.compile('&failCode=(\d+)')

        print ('Login...')
        while not isLogin:
        	#write validation code image to local image file
            validation = self.opener.open(Config.ICODEURL).read()
            with open('icode.jpg', 'wb') as file:
                file.write(validation)
            icode = input('Please input the validation code shown in icode.jpg: ')
            data['icode'] = icode
            
            #create a request, then open the url
            request = urllib.request.Request(Config.LOGINURL, urllib.parse.urlencode(data).encode(encoding='utf-8'))
            response = self.opener.open(request, timeout=20)

            url = response.geturl()
            print (url)
            failCode = failCodePattern.search(url)
            if not failCode:
                for item in self.cookie:
                    if item.name == 'id':
                        self.userID = item.value
                        print ('Login Successfully')
                        self.cookie.save(PrivateConfig.CookieFile, ignore_discard=True, ignore_expires=True)
                        isLogin = True
                        break
            else:
                failCode = faileCode.group(1)
                if failCode in Config.FAILCODE.keys():
                    print ('Error: failCode = ', failCode, ' ', Config.FAILCODE[failCode])
                    if failCode == '512':  ##validation code is wrong
                        continue
                else:
                	print ('Error: Unknown error')
                return False
        return True
    
    def getRawContent(self, url, data = None):
        try:
            print('url: ', url)
            print('data: ', data)
            page = self.opener.open(url, data, timeout = 20)
        except Exception as e:
            print ('Fail to login: ', e)
            return
        return page

    def getContent(self, url, data = None):
        return self.getRawContent(url, data).read()	
    
    def getUserID(self):
        return self.userID

'''
   if this .py file is executed directly, the following code after if __name__ == '__main__' will be excuted,
   if this .py file is loaded as a module, the following code after if __name__ == '__main__' will not be executed
'''
if __name__ == '__main__':
   baobao = RenrenSpider()
   baobao.login() 	

 
