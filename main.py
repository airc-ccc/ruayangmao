#!/usr/bin/python3

import os
import sys
import requests
import qrcode
import datetime
import argparse

parser = argparse.ArgumentParser(description='Process some params.')

parser.add_argument('-u', type=str, required=True,
                    help='fufuzhuan username')

parser.add_argument('-p', type=str, required=True,
                    help='fufuzhuan password')

parser.add_argument('-gn', type=int, required=True,
                    help='you have wechat group numbner.')

args = parser.parse_args()

userCode = args.u
userPass = args.p
wechatGroupNumber = args.gn
setSuccess = 'http://sm.ewmtool.com/insertRecord?codeSuccess=0&recordId='
setError = 'http://sm.ewmtool.com/insertRecord?codeSuccess=1&recordId='
# now date time
nowDate = datetime.datetime.now().strftime("%Y-%m-%d")
nowTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%i:%s")

# Login POST
getLogin = requests.post('http://sm.ewmtool.com/getLogin', data={'userCode': userCode, 'userPass': userPass})
if getLogin.json()['code'] != 200:
    print(getLogin.json())
    sys.exit()
print(getLogin.json())

# put wechat group number
userDayCount = requests.post('http://sm.ewmtool.com/userDayCount', data={'number': wechatGroupNumber}, cookies=getLogin.cookies)
if userDayCount.json()['code'] != 200:
    print(userDayCount.json())
    sys.exit()
print(userDayCount.json())

savePath = './qrcode/' + nowDate + '/'

if not os.path.exists(savePath):
    os.makedirs(savePath)

saveDataPath = './data/'
if not os.path.exists(saveDataPath):
    os.makedirs(saveDataPath)

dataFile = open('./data/data-'+nowDate+'.json', 'a')
gone = True
while(gone):
# get qr code
    getQr = requests.post('http://sm.ewmtool.com/getQr', cookies=getLogin.cookies)

    jsonData = getQr.json()
    if jsonData['code'] != 200:
        print(jsonData)
        gone=False
        break
    print(jsonData)
    dataFile.write(nowTime+'===='+getQr.text+"\n")
    # make code 
    img = qrcode.make(jsonData['data']['imgsrc'])
    img.save(savePath + jsonData['data']['name'] + '.png')

    print("------------------------------------------------------------")


