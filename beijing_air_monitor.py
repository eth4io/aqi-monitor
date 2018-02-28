# coding:utf-8

import requests
import re
import time
import random
import json
import telegram

AQICN_BASE_URL = "https://api.waqi.info"
CITY_FEED = "/feed/{}/?token={}"

LEVEL_GOOD = "Good"
LEVEL_MODERATE = "Moderate"
LEVEL_UNHEALTHY_FOR_SENSITIVE_GROUPS = "Unhealthy for Sensitive Groups"
LEVEL_UNHEALTHY = "Unhealthy"
LEVEL_VERY_UNHEALTHY = "Very Unhealthy"
LEVEL_HAZARDOUS = "Hazardous"
LEVEL_BEYOND_INDEX  = "Beyond Index"


def get_aqi_data():
    city = "@3303"  # Beijing US Embassy
    url = "{}{}".format(AQICN_BASE_URL, CITY_FEED.format(city, AQICN_TOKEN))
    response = requests.get(url=url)
    data = json.loads(response.text)
    print(data)
    if 'status' not in data:
        raise ValueError("no status in city feed response json")
    if 'data' not in data:
        raise ValueError("no data in city feed response json")
    if 'time' not in data['data']:
        raise ValueError("no time in city feed response json")
    elif 's' not in data['data']['time']:
        raise ValueError("no s.time in city feed response json")
    time = data['data']['time']['s']
    if 'aqi' not in data['data']:
        raise ValueError("no aqi in city feed response json")
    aqi = data['data']['aqi']
    if 'iaqi' not in data['data']:
        raise ValueError("no iaqi in city feed response json")
    elif 'pm25' not in data['data']['iaqi']:
        raise ValueError("no pm25 in city feed response json")
    elif 'v' not in data['data']['iaqi']['pm25']:
        raise ValueError("no v.pm25 in city feed response json")
    pm25 = data['data']['iaqi']['pm25']['v']

    if aqi <= 50 & aqi > 0:
        level = LEVEL_GOOD
    elif aqi <= 100:
        level = LEVEL_MODERATE
    elif aqi <= 150:
        level = LEVEL_UNHEALTHY_FOR_SENSITIVE_GROUPS
    elif aqi <= 200:
        level = LEVEL_UNHEALTHY
    elif aqi <= 300:
        level = LEVEL_HAZARDOUS
    else:
        level = LEVEL_BEYOND_INDEX

    str = "{}; AQI: {}; PM2.5: {}; {}".format(time, aqi, pm25, level)
    return str


if '__name__==__main__':
    global isDebug
    global AQICN_TOKEN
    global BOT_API
    global TESTER_ID
    global CHANNEL_ID
    isDebug = False
    try:
        with open('config.json') as config_json:
            config = json.load(config_json)
            if config["debug_mode"].lower() == 'true'.lower():
                isDebug = True
            AQICN_TOKEN = config["aqicn_token"]
            BOT_API = config["bot_token"]
            TESTER_ID = config["tester_id"]
            CHANNEL_ID = config["channel_id"]
    except Exception as e:
        print(e)

    bot = telegram.Bot(BOT_API)
    if isDebug:
        commit_token = TESTER_ID
    else:
        commit_token = CHANNEL_ID
    # bot.send_message(commit_token, "test")
    print(bot.get_me())

    print(get_aqi_data())

    # while 1:
    #     try:
    #         get_data()
    #     except Exception as ex:
    #         print(ex)
    #     if isDebug:
    #         sleep_duration = 5
    #     else:
    #         sleep_duration = 3600 + random.randint(-300, 300) # 1h ± 5min
    #     time.sleep(sleep_duration)
