# coding:utf-8

import requests
import time
import json
import telegram
from aqi_data import AqiData

AQICN_BASE_URL = "https://api.waqi.info"
CITY_FEED = "/feed/{}/?token={}"

SHORT_SLEEP_DURATION = 300
LONG_SLEEP_DURATION = 2400


def get_aqi_data():
    url = "{}{}".format(AQICN_BASE_URL, CITY_FEED.format(CITY, AQICN_TOKEN))
    response = requests.get(url=url)
    data = json.loads(response.text)
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

    aqi_data = AqiData(time, aqi, pm25)

    return aqi_data


if '__name__==__main__':
    global isDebug
    global AQICN_TOKEN
    global BOT_API
    global TESTER_ID
    global CHANNEL_ID
    global CITY
    global lastUpdateTime
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
            CITY = config["city"]
            lastUpdateTime = ""
    except Exception as e:
        print(e)

    bot = telegram.Bot(BOT_API)

    while 1:
        try:
            if isDebug:
                commit_token = TESTER_ID
            else:
                commit_token = CHANNEL_ID

            aqi_data = get_aqi_data()
            if aqi_data.time != lastUpdateTime:
                message = "{}; AQI: {}; PM2.5: {}; {}".format(aqi_data.time, aqi_data.aqi, aqi_data.pm25,
                                                              aqi_data.level)
                bot.send_message(commit_token, message)
                lastUpdateTime = aqi_data.time
                if isDebug:
                    sleep_duration = 60
                else:
                    sleep_duration = LONG_SLEEP_DURATION
                time.sleep(sleep_duration)
            else:
                if isDebug:
                    sleep_duration = 60
                else:
                    sleep_duration = SHORT_SLEEP_DURATION
                time.sleep(sleep_duration)
        except Exception as ex:
            print(ex)
