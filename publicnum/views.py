from django.shortcuts import render

# 引用用到的库
import time
from django.http import HttpResponse           #进行简单的http应答
from urllib.request import urlopen                           
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
                elif '天气'   in content  :
                    content=mypack.weather(content)
                elif '单词' in content :
                    word=content[2:]
                    content=content[2:]
                    print(word)
                    with open('words.txt','a') as file:
                        file.write('\n'+word)
                else:
                    message=content
                    content=mypack.talks_robot(message)
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