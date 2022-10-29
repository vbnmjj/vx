from django.shortcuts import render

# 引用用到的库
from django.http import HttpResponse           #进行简单的http应答
from urllib.request import urlopen 
import time                                    #导入时间计算模块计算access_token结束时间
import xmltodict
from urllib.request import urlopen
from  bs4 import BeautifulSoup as soup
from . import mypack
#还没写好
def reply(request):
    try:                            #尝试获取验证参数
        signature = request.GET.get('signature')
       
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        authcode=mypack.auth(nonce,timestamp)
    except:
        return HttpResponse("error")
    if signature!=authcode:         #验证是否是来自微信的消息
        return HttpResponse("error")
    else :                          #验证成功
        if request.method=='GET':   #如果是get返回echostr验证
            return HttpResponse(request.GET.get('echostr'))
        else:
            request.method=='POST'#表示是微信服务器转发
            xml_dict=xmltodict.parse(request.body.decode())
            xml_dict=xml_dict.get('xml')
          
            type=xml_dict.get('MsgType')
            tousername=xml_dict.get('ToUserName')
            fromusername=xml_dict.get('FromUserName')
            if type != 'voice':
                content=xml_dict.get('Content')
                #确定发送内容
                if content =='hello':
                    content='helloboy'
                    print('helloboy')
                elif type =='event':
                    content='开始使用吧'
                elif type !='text':
                    content='暂时不支持该消息'
                elif '天气'   in content and '机器人' not in content :
                    content=mypack.weather(content)
                elif '饭'  in content or '吃' in content :
                    content=mypack.lunch()
                elif '马义' in content :
                    content='姓马名义'
                elif '机器人' in content:
                    message=content[3:]
                    content=mypack.talks_robot(message)
                elif '单词' in content :
                    word=content[2:]
                    content=content[2:]
                    print(word)
                    with open('words.txt','a') as file:
                        file.write('\n'+word)
                resp_dict='''
                <xml>
                    <ToUserName><![CDATA[{}]]></ToUserName>
                    <FromUserName><![CDATA[{}]]></FromUserName>
                    <CreateTime>{}</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[{}]]></Content>
                </xml>'''.format(fromusername,tousername,int(time.time()),content)
            elif  type=='voice' :
                voice_id=xml_dict.get('MediaId')
                print(voice_id)
                resp_dict='''
                <xml>
                <ToUserName><![CDATA[{}]]></ToUserName>
                <FromUserName><![CDATA[{}]]></FromUserName>
                <CreateTime>{}</CreateTime>
                <MsgType><![CDATA[voice]]></MsgType>
                <Voice>
                    <MediaId><![CDATA[{}]]></MediaId>
                </Voice>
                </xml>'''.format(fromusername,tousername,int(time.time()),voice_id)
            return HttpResponse(resp_dict)

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
'''
222.137.129.236 ipv6 ::ffff:222.137.129.236,
 
class Wechat():
    def __init__(self):
        self.overtime=0
        self.token_str=' '
    
    #读取access_token
    def read_access_token(self):
        try :
            with open('save_token.txt','r') as file :
                self.token_str=file.readlines()
        except:
            return False
    #查看时间是否过期
    def is_valid(self):
        if self.token_str =='hello':
            return False
        return self.overtime > time.time()
test=Wechat()
test.read_access_token()
if test.token_str == 'hello' or  test.overtime >time.time():
    print(test.token_str,test.overtime)
    test.get_acess_toen()
    test.read_access_token
    print('yes it is update')
else:
    print(test.token_str,test.overtime)
    print('yes it is right')

        
    

#---------------------------------------------------------------------------------------------------- 
'''