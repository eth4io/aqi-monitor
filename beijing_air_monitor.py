# coding:utf-8

import requests
import re
import time
import random
import json
import telegram





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
    bot.get_updates()

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