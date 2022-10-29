from urllib.request import urlopen
from  bs4 import BeautifulSoup as soup
import json  
import requests
from random import randint
import hashlib   #进行哈希加密
#验证token的
def auth(nonce,timestamp):
    token = "fenghaojie" #请按照公众平台官网\基本配置中信息填写
    list = [nonce,timestamp,token]
    list.sort()
    sha1 = hashlib.sha1()
    new=(''.join(str(i) for i in list))
    sha1.update(new.encode('utf-8'))
    hashcode = sha1.hexdigest()
    return hashcode
def weather(content):
    url={'郑州':'https://tianqi.2345.com/tomorrow-57083.htm',
    '盐城':'https://tianqi.2345.com/today-58151.htm',
    '上海':'https://tianqi.2345.com/today-58362.htm',
    '长春':'https://tianqi.2345.com/today-54161.htm',
    '连云港':'https://tianqi.2345.com/today-58044.htm',
    }
    try :
        if content[0:2] in url:
            content=content[0:2]
        elif content[0:3] in url:
            content=content[0:3]
        elif content[0:4] in url:
            content=content[0:4]
        resp=urlopen(url[content])
    except:
        return '🌕🌖🌗🌘🌔🌒🌑'
    html=soup(resp,'html.parser')
    a_list=html.find_all('a',{'class':'seven-day-item'})
    string='☀ ☼ ♨☁ ☂☽ ☾❄ ❅ ❆ ☃'
    #'🌞🌝🌛🌜🌚🌕🌖🌗🌘🌔🌒🌑🌙☀🌤⛅🌥☁🌦🌧⛈🌩🌨❄🌟⚡💧☔🌈🌊🌫🌪☄🪐')
    for i in a_list:
        day=i.get_text().split()
        if day[2]=='晴':
            day[2]+='☀'
        elif day[2] =='晴转多云':
             day[2]+='☀🌥'
        elif day[2]=='多云':
            day[2]+='⛅🌥'
        elif day[2]== '多云转中雨' or '多云转大雨':
            day[2]+='🌥🌧'
        elif day[2] =='多云转阴':
            day[2]+='⛅☁'
        elif day[2] == '小雨转大雨' or '小雨转中雨':
            day[2]+='🌦🌧'
        elif day[2]:
            pass
        string=string+'''

{}|{} |{}
天气: {}
🌈温度:{}
🌪风度：{}  
空气质量：{}
🧡💛❤'''.format(content,day[0],day[1],day[2],day[3],day[4],day[5])
    return string


def talks_robot(content = '你叫什么名字', source = '0'):
    api_url = 'http://www.tuling123.com/openapi/api'         #https://werobot.readthedocs.io/zh_CN/latest/start.html 这个是开发文档
    api_key = '8cbd75edbcb3477dab307106240ae53e' #请填入自己申请的图灵付费api_key
    data = {'key': api_key, 'info': content, 'userid': 'hello'}  
    data=json.dumps(data) 
    req = requests.post(api_url, data=data).text
    reply = json.loads(req)['text']
    return reply

#回复吃饭
def lunch():
    with open('lunch.txt') as file:
        foodlist=file.readlines()
        num=randint(0,len(foodlist))
        print(num,len(foodlist))
        food=foodlist[num].split()
        food= '''🐷名字:{}
作者：{}
🍢{}
教程:{}'''.format(food[0],food[1],food[2],food[3])
        return food