# -*- coding: utf-8 -*-
import os
import json
import re
import time

def CreatePath(path): 
    if not os.path.exists(path): 
            os.mkdir(path)

def IsPathExist(path):
    return os.path.exists(path)

def RemoveFile(path):
    if IsPathExist(path):
        os.remove(path)    

'''
    服务器返回的是html格式数据，不是json格式，之后通过beautifulsoup查询获得其中需要的json数据的时候，
    这种从html中获得的json数据格式是有问题不完全满足json格式的，因此需要用这个函数进行转化

    json.loads 用于解码 JSON 数据，将满足json格式要求的str类型的数据转成python中的dictionary类型。
    当我们用requests请求一个返回json的接口时候，得到的结果中包含了一串让人看
    不懂的东西 \\uxxxx的，这是中文对应的unicode编码形式。json.loads()就可以把他们转化为中文
'''
def generateJson(rawContent):
    '''
        获得数据部分内容，通过观察chrome开发者工具element中的html知道，
        第一个'{'和'};'中的内容就是完整的数据
    '''
    content = rawContent[rawContent.find('{') : rawContent.find('};')+1]  #不包括上界，因此要+1
    '''
        过观察chrome开发者工具element中的html知道，人人网解析出来的content中
        并不是严格使用双引号，所以需要将出现的单引号替换为双引号。
        但是用replace替换的话有一个地方会对结果造成干扰
        （见下，单引号全部替换后，由于http后面有“:”，会使得json报错）
        所以用单引号之前有没有“=”来判断是否需要转换，具体步骤见如下循环
        "title":"<img src='http://a.xnimg.cn/imgpro/icons/statusface/zongzi.gif' alt='测试'  />测试用例测试用例\n"
        content = content.replace("'",'"')
    '''
    newContent = ''
    i = -1
    for j in range(0, len(content)):
        if i == -1:
            if content[j] != "'":
                newContent += content[j]
            else:
                i = j;
        else:
            if content[j] == "'":
                if i-1 >= 0 and content[i-1] == '=':
                    newContent += content[i:j+1]
                else:
                    newContent += '"' + content[i+1:j] + '"'
                i = -1
    return json.loads(newContent)	#json.loads()用于将str类型的数据转成dictionary


def validateFilename(rawName):
    "替换不能用在文件路径中的非法字符"
    illegalStr = r"[\:|]"    #python中文件路径中的非法字符 '/ \ : * ? " < > |'
    legalName = re.sub(illegalStr, "_", rawName)    #将非法字符替换为下划线
    return legalName

def timestampToLocaltime(timestamp):
    "时间戳转换成localtime"
    timeLocal = time.localtime(timestamp)
    #转换成新的时间格式(2016-05-05 20:28:54)
    datetime = time.strftime("%Y-%m-%d %H:%M:%S",timeLocal)
    return datetime