# -*- coding: utf-8 -*-
import time
from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
from getweather import fetchWeather

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['POST', 'GET'])
def wechat():
    if request.method=='GET':
        data = request.args
        token = 'livingworld' #设置公众号token  

        signature = data.get('signature','') #微信加密签名
        timestamp = data.get('timestamp','') #时间戳
        nonce = data.get('nonce','') #随机数
        echostr = data.get('echostr','') #随机字符串
        
        list = [timestamp,nonce,token]
        list.sort()
        s = ''.join(list)
        s = s.encode('utf-8')
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    else:
        xml_recv = ET.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text
        FromUserName = xml_recv.find("FromUserName").text
        Content = xml_recv.find("Content").text
        xml_rep = "<xml>\
                    <ToUserName><![CDATA[%s]]></ToUserName>\
                    <FromUserName><![CDATA[%s]]></FromUserName>\
                    <CreateTime>%s</CreateTime> \
                    <MsgType><![CDATA[text]]></MsgType>\
                    <Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag>\
                    </xml>"

        if Content.strip() == '帮助':
            response = make_response(xml_rep % (FromUserName,ToUserName,
                                                str(int(time.time())),help()))
            response.Content_type='application/xml'
            return response

        elif Content.strip() == '历史':
            response = make_response(xml_rep % (FromUserName,ToUserName,
                                                str(int(time.time())),history()))
            response.Content_type='application/xml'
            return response

        else:
            response = make_response(xml_rep % (FromUserName,ToUserName,
                                                str(int(time.time())),weather(Content)))
            response.Content_type='application/xml'
            return response

def weather(content):
    #try:
    result = fetchWeather(content)
    text = "{}的天气情况：{}; \n温度：{}℃; \n更新时间：{} \n".\
        format(result["results"][0]["location"]["name"],result["results"][0]["now"]["text"],["results"][0]["now"]["temperature"],result["results"][0]["last_update"])
    historyList.append(text)

    #except Exception as e:
     #   helpText = help()
    #text = '搜索不到您要的信息，请参照帮助信息操作。\n 帮助：\n' + helpText

    return text

def help():
    help = '输入城市中文名称查询天气信息；\n' \
           '输入「帮助」获取帮助信息；\n' \
           '输入「历史」获取历史信息。'
    return help

def history():
    text = ' '.join(historyList)
    return text

if __name__ == '__main__':
    historyList = []
    app.run(debug=True, host='0.0.0.0', port=80)