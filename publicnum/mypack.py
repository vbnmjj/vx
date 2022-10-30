from tkinter import E
from urllib.request import urlopen
from  bs4 import BeautifulSoup as soup
import json  
import requests
from random import randint
import hashlib   #进行哈希加密
import time         #导入时间计算模块计算access_token结束时间
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
    head={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
    try:
        sess = requests.get('https://api.ownthink.com/bot?appid=xiaosi&spoken=%s'%content,headers=head)
        answer = sess.text
    except:
        answer={'message': 'success', 'data': {'type': 5000, 'info': {'text': '亲娘嘞,服务暂停了'}}}
    answer =(json.loads(answer))["data"]
    return answer["info"]["text"]

#----------------------------------------------------------回复吃饭-----------------------------------------------
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
def get_acess_token():
        #定义请求地址
        url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx7ce93198fa95c2b5&secret=66f5ea9b06da6e7fbc11fd0fa8f50f05'
        html=urlopen(url)
        html=html.read().decode()
        first_dict=eval(html)         #read()之后是字节 decode() 或者str()都可以转换成字符串  再用eval转换为字典
                                        #econd_dict=json.loads(html.read().decode())  #两种方式将字典格式的字符串转换为字典 
        #接收响应  拿到 access_token  expires_in
        res=first_dict
        print(res)
        #设置过期时间
        overtime=time.time()+res['expires_in']-300
        with open('save_token.txt','w') as file:
            file.writelines(res['access_token'])