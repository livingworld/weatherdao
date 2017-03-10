import json
import sys
import requests
import time

history_weather_list=[]#历史天气查询记录list
def dumpTianqi(result):
    #最后进行解析
    dic = result
    city=dic["results"][0]["location"]["name"]
    weather=dic["results"][0]["now"]["text"]
    temperature=dic["results"][0]["now"]["temperature"]
    updates=dic["results"][0]["last_update"]
    weather_info = "%s 的天气情况是：%s，温度是：%s℃，数据更新时间为：%s" % (city, weather, temperature, updates)
    history_weather_list.append(weather_info)
    return weather_info

'''result = requests.get(url, params, timeout)，发送get请求'''
def fetchWeather(location):
    API = 'https://api.thinkpage.cn/v3/weather/now.json'
    KEY='xl42ljwdjatghvnw'
    LANGUAGE='zh-Hans'
    UNIT='c'
#通过 parse 将请求参数转为字符串
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT
    })
    result = result.text
    result = json.loads(result)
    return result

def history_weather():
    history_weather_info=history_weather_list
    #for item2 in history_weather_list:
    #    history_weather_info='\n'.join(history_weather_list)
    return history_weather_info#以字符串形式返回历史查询记录

def help_weather():
    return '''输入城市名或拼音，点击"查询按钮获取该城市的天气情况；
            点击"帮助"按钮,获取帮助文档；
            点击"历史"查询按钮,获取查询历史；
            点击"离开"，退出天气查询系统。'''

def quit_weather():
    return quit()