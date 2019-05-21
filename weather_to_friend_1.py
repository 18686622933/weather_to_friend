from wxpy import *
import requests
from datetime import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler  # 定时框架
from urllib.request import urlopen
from bs4 import BeautifulSoup

bot = Bot(cache_path=True)  # 登陆微信
tuling = Tuling(api_key='4a0488cdce684468b95591a641f0971d')  # 机器人api


"""
# 单个好友
friend = bot.friends().search('李瑞彤')[0]#好友的微信昵称，或者你存取的备注
location = friend.city  # 获取好友地址
friends = bot.groups().search('百事可乐')[0]  # 获取群
"""


# 好友列表
# friendlist = [ensure_one(bot.search(remark_name='李瑞彤')), bot.friends().search(remark_name='李瑞彤')[0],
#               bot.friends().search(remark_name='戴文')[0],
#               bot.friends().search(remark_name='唐')[0]
#               ]



def get_weather(location):
    """获取天气信息，传入地址函数location"""
    # 准备url地址，得出location的结果
    path = 'http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'
    url = path % location
    response = requests.get(url)
    result = response.json()
    str1 = '    你的城市: %s\n' % location

    # 如果城市错误就按照成都的结果
    if result['error'] != 0:
        str1 = '    你的地区%s获取失败，请修改资料。默认参数：长春\n' % location
        location = '长春'
        url = path % location
        response = requests.get(url)
        result = response.json()

    str0 = ('    这是明天的天气预报！\n')
    results = result['results']
    # 取出数据字典
    data1 = results[0]
    # 取出pm2.5值
    pm25 = data1['pm25']
    str2 = '    PM2.5 : %s  ' % pm25
    # 将字符串转换为整数 否则无法比较大小
    pm25 = int(pm25)
    if pm25 == '':
        pm25 = 0
    # 通过pm2.5的值大小判断污染指数
    if 0 <= pm25 < 35:
        pollution = '优'
    elif 35 <= pm25 < 75:
        pollution = '良'
    elif 75 <= pm25 < 115:
        pollution = '轻度污染'
    elif 115 <= pm25 < 150:
        pollution = '中度污染'
    elif 150 <= pm25 < 250:
        pollution = '重度污染'
    elif pm25 >= 250:
        pollution = '严重污染'
    str3 = '    空气指数: %s\n' % pollution
    result1 = results[0]
    weather_data = result1['weather_data']
    data = weather_data[1]
    datetime = data['date']
    temperature = data['temperature']
    str4 = '    明天温度: %s%s\n' % (datetime, temperature)
    wind = data['wind']
    str5 = '    风向 : %s\n' % wind
    weather = data['weather']
    str6 = '    天气 : %s\n' % weather
    #  str7 ='    温度 : %s\n' % data['temperature']
    message = data1['index']
    str8 = '    穿衣 : %s\n' % message[0]['des']
    # str9 ='    我很贴心: %s\n' % message[2]['des']
    # str10 ='    运动 : %s\n' % message[3]['des']
    str11 = '    紫外线 : %s\n' % message[4]['des']
    # str12="\n   请注意身体~\n"
    str = str0 + str1 + str2 + str3 + str4 + str5 + str6 + str8 + str11
    return str


def get_iciba():
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    str = '    每日一句：\n' + content + '\n' + note + '\n'
    return str


# 原函数，未使用
def send_message0():
    friend = bot.groups().search('百事可乐')[0]  # 获取群
    location = '长春'
    # print(i + 1, '/%s' % len(friend), ' 姓名：%s' % friend, ' 地区：%s' % location)
    # text = get_weather(location) + get_iciba() + '    ~'    # 带每日一句
    text = get_weather(location)        # 不带每日一句
    friend.send(text)
    # 发送成功通知我
    bot.file_helper.send(friend)
    bot.file_helper.send('发送完毕')  # 发送到微信助手
    return


# 我的函数，简化部分内容
def send_message1():
    name = '百事可乐'
    location = '长春'
    person_or_group = 1
    if person_or_group == 1:
        bot.groups().search(name).send(get_weather(location))
    else:
        bot.friends().search(name).send(get_weather(location))
    bot.file_helper.send(str(name) + '    已发送')


def send_message2():
    name = 'sunshine*'
    location = '上海'
    bot.friends().search(name)[0].send(get_weather(location))
    bot.file_helper.send(str(name) + '发送完毕')
    return

def send_message3():
    name = '李瑞彤'
    location = '长春'
    bot.friends().search(name)[0].send(get_weather(location))
    bot.file_helper.send(str(name) + '发送完毕')
    return


# 带参数，未使用
def send_message(per_or_gro, name, location):
    """极简写法，但不能用于定时"""
    if per_or_gro == 'g':
        bot.groups().search(name)[0].send(get_weather(location))
    else:
        bot.friends().search(name)[0].send(get_weather(location))
    bot.file_helper.send(str(name) + '发送完毕')
    return


# 多人
# def send_messages():
#     """目标为多人时"""
#     for i in range(len(friendlist)):
#         friend = friendlist[i]
#         location = friend.city
#         print(i + 1, '/%s' % len(friendlist), ' 姓名：%s' % friend, ' 地区：%s' % location)
#         text = get_weather(friend.city) + get_iciba() + '    好梦~'
#         friend.send(text)
#         # 发送成功通知我
#         bot.file_helper.send(friend)
#         bot.file_helper.send('发送完毕')
#     return



# 定时器
print('start')
sched = BlockingScheduler()
sched.add_job(send_message1, 'cron', day_of_week='0-6', hour=16, minute=50)  # 设定发送的时间
sched.add_job(send_message2, 'cron', day_of_week='0-6', hour=19, minute=0)
sched.add_job(send_message3, 'cron', day_of_week='0-6', hour=14, minute=30)

sched.start()