from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from dateutil.utils import today

start_date = os.environ['START_DATE']
month = "02-01"
city = os.environ['CITY']
birthday_female = "02-10"
birthday_male = "04-20"
key = "7f4e76064b4442f929c616ecb0dfc591"

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ID = "o6Y0v5rgQYUcZCyOUFRteM6Sp4ec"
tem_id = "3Ead6cyC1Btz6QewVi4z8qf_rwnZBZvZTLu8MXOiBQc"

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]




def get_cai():
  response = requests.get(url='https://api.tianapi.com/caihongpi/index?key=' + key).json()
  return response["newslist"][0]['content']


def get_birthday(birthday):
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today()).days


def get_togetherTime():
  next = datetime.strptime(start_date, "%Y-%m-%d")
  return (today() - next).days


def get_togetherYear():
    t = datetime.strptime(str(today().year) + "-" + month, "%Y-%m-%d")
    together = datetime.strptime(start_date, "%Y-%m-%d")
    if (today() - t).days > 0:
        return "距离张小姐和孙先生的"+str(today().year - together.year + 1)+"周年还有"+str((datetime.strptime(str(today().year+1) + "-" + month, "%Y-%m-%d") - today()).days) + "天"
    elif (today() - t).days == 0:
        return "今天是张小姐和孙先生的"+str((today().year-together.year))+"周年"
    else:
        return "距离张小姐和孙先生的"+str(today().year - together.year)+"周年还有" + str((t-today()).days) + "天"


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather


def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


def get_date():
  d = datetime.today()  # 获取当前日期时间
  week = d.isoweekday()
  date = today().strftime("%Y-%m-%d")
  if week == 1:
    return date + " 星期一"
  if week == 2:
    return date + " 星期二"
  if week == 3:
    return date + " 星期三"
  if week == 4:
    return date + " 星期四"
  if week == 5:
    return date + " 星期五"
  if week == 6:
    return date + " 星期六"
  if week == 7:
    return date + " 周日"


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
data = {"date": {"value": get_date(), "color": get_random_color()},
        "city": {"value": city, "color": get_random_color()},
        "weather": {"value": get_weather()['weather'], "color": get_random_color()},
        "min_temperature": {"value": str(get_weather()['low']) + "℃", "color": get_random_color()},
        "max_temperature": {"value": str(get_weather()['high']) + "℃", "color": get_random_color()},
        "pipi": {"value": get_cai().replace("XXX","张小姐"), "color": get_random_color()},
        "love_day": {"value": get_togetherTime(), "color": get_random_color()},
        "birthday1": {"value": get_birthday(birthday_female), "color": get_random_color()},
        "birthday2": {"value": get_birthday(birthday_male), "color": get_random_color()},
        "year": {"value": get_togetherYear(), "color": get_random_color()},
        }
res = wm.send_template(user_id, template_id, data)
print(res)
res = wm.send_template(user_ID, tem_id, data)
print(res)
