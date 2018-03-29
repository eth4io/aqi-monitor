# coding:utf-8

import requests
import time
import json
import telegram
import datetime
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
    iaqi = data['data']['iaqi']
    if 'pm25' not in iaqi:
        raise ValueError("no pm25 in city feed response json")
    elif 'v' not in data['data']['iaqi']['pm25']:
        raise ValueError("no v.pm25 in city feed response json")
    pm25 = iaqi['pm25']['v']
    if 'pm10' not in iaqi:
        raise ValueError("no pm10 in city feed response json")
    elif 'v' not in iaqi['pm10']:
        raise ValueError("no v.pm10 in city feed response json")
    pm10 = iaqi['pm10']['v']

    aqi_data = AqiData(time, aqi, pm25, pm10)

    return aqi_data


def init():
    global isDebug
    global AQICN_TOKEN
    global BOT_API
    global TESTER_ID
    global CHANNEL_ID
    global CITY
    global CONFIG_LAST_UPDATE_TIME
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
            CONFIG_LAST_UPDATE_TIME = config["last_update_time"]
    except Exception as e:
        print(e)


def start():
    last_update_time = CONFIG_LAST_UPDATE_TIME
    bot = telegram.Bot(BOT_API)
    while 1:
        try:
            if isDebug:
                commit_token = TESTER_ID
            else:
                commit_token = CHANNEL_ID

            aqi_data = get_aqi_data()
            timestamp = datetime.datetime.now()
            if aqi_data.time != last_update_time:
                message = "{}; PM2.5: *{}*; PM10: *{}*; {}".format(aqi_data.time, aqi_data.pm25, aqi_data.pm10,
                                                              aqi_data.level)
                print(str(timestamp) + " new data: " + message)
                bot.send_message(chat_id=commit_token, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
                last_update_time = aqi_data.time
                if isDebug:
                    sleep_duration = 5
                else:
                    sleep_duration = LONG_SLEEP_DURATION
                time.sleep(sleep_duration)
            else:
                print(str(timestamp) + " same time as last_update_time: " + aqi_data.time)
                if isDebug:
                    sleep_duration = 5
                else:
                    sleep_duration = SHORT_SLEEP_DURATION
                time.sleep(sleep_duration)
        except Exception as ex:
            print(ex)
            time.sleep(SHORT_SLEEP_DURATION)


if '__name__==__main__':
    init()
    start()
