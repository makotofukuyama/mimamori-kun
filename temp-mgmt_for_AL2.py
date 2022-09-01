#!/usr/bin/env python3
# coding: utf-8

# from os import set_handle_inheritable
import time
import redis
import datetime         #debug
# import schedule
from time import sleep
import requests
from requests.structures import CaseInsensitiveDict

#####  Set constant values for Radis  #####################

RedisKey = "RPIvalue"

##########################
### For using RadisLabs
### You need to change RedisHost,RedisPort and RedisPwd below

RedisHost = "xxxxxxx.redislabs.com"  
RedisPort = "xxxxx"
RedisPwd = "xxxxxxxxxxxxxxxxxxxx"
##########################

###########################################################
#####  Define functions   #################################

def check_db():
    ### Check Redis connection 
    r = redis.Redis(host=RedisHost, port=RedisPort, password=RedisPwd, db=0)
    print("Connected Radis...: " + RedisHost)
    ### Check Redis Key
    ret = r.get(RedisKey)
    # print (ret)                             ### for debug
    if ret is None:                         # if no exist RedisKey                 
        print("Failed Key: " + RedisKey)
        return ret                          # Return Value
    msg = str(ret.decode("utf-8"))
    print("Key:" + RedisKey + "Value:" + msg)
    return ret

def get_db():                            ### get data from Redis 
    r = redis.Redis(host=RedisHost, port=RedisPort, password=RedisPwd, db=0)
    now_t = (datetime.datetime.now()).strftime("%m/%d %H:%M")  #debug 
    # r.get(RedisKey ,msg)                   
    RPitemp = r.get(now_t) 
    return RPitemp

def linenotify():
    url = "https://notify-api.line.me/api/notify" 
    token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    headers = {"Authorization" : "Bearer "+ token} 
    message =  "現在の温度は" + str(inputValue.decode("utf-8")) + "℃です。ヒーターの電源を" + dengenjyoutai + "に変更しました"
    payload = {"message" :  message} 
    r = requests.post(url, headers = headers, params=payload)


def switchbotpoweron():

    url = "https://api.switch-bot.com/v1.0/devices/xxxxxxxxxxxx/commands"

    headers = CaseInsensitiveDict()
    headers["Authorization"] = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    headers["Content-Type"] = "application/json; charset=utf8"

    data = '{  "command": "turnOn",  "parameter": "default",  "commandType": "command"}'


    resp = requests.post(url, headers=headers, data=data)

    print(resp.status_code)


def switchbotpoweroff():

    url = "https://api.switch-bot.com/v1.0/devices/xxxxxxxxxxxxx/commands"

    headers = CaseInsensitiveDict()
    headers["Authorization"] = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    headers["Content-Type"] = "application/json; charset=utf8"

    data = '{  "command": "turnOff",  "parameter": "default",  "commandType": "command"}'


    resp = requests.post(url, headers=headers, data=data)

    print(resp.status_code)


def ondohyouji():
    print(now_t, end="   ")
    print(inputValue.decode("utf-8"))

def jyoutaihyouji():
    print ("現在の電源は"+dengenjyoutai+"の状態です")




###########################################################
#####  初期設定　　　　　　      ###########################
kijun = float(30.00)        # 温度基準値℃
dengenjyoutai = "OFF"       # 電源状態。"ON"または"OFF"
###########################################################

###########################################################
#####  Main                     ###########################

while True:
    inputValue = get_db()
    now_t = (datetime.datetime.now()).strftime("%m/%d %H:%M") 
    if inputValue is None:
        print ("No data on Redis")
        # print (now_t, "No data on Redis")   # for debug
    elif float(inputValue) < kijun and dengenjyoutai == "OFF" :             #　turnon処理。
        jyoutaihyouji()
        ondohyouji()
        print("turnon処理をします")                                           # for debug
        switchbotpoweron()
        dengenjyoutai = "ON"                                                # 電源状態をオンに変更
        linenotify()
        print ("電源の状態を ", dengenjyoutai, "に変更しました")              # for debug        
        sleep(55)                                                           # 一度通知したら55秒休む(合計１分)
    elif float(inputValue) >= kijun and dengenjyoutai == "ON" :             #　turnoff処理。
        jyoutaihyouji()
        ondohyouji()                                              # for debug
        print("turnoff処理をします")                                         # for debug
        switchbotpoweroff()
        dengenjyoutai = "OFF"                                                # 電源状態をオフに変更
        linenotify()
        print ("電源の状態を ", dengenjyoutai, "に変更しました")                 # for debug        
        sleep(55)                           # 一度通知したら55秒休む(合計１分)
    else:                                       # 状態に変化がない場足の処理（No action）
        jyoutaihyouji()
        ondohyouji()       
        print("No actionです")                                         # for debug
    sleep(5)

###########################################################






