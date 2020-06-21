#!/usr/bin/python3

import os
import requests
import qrcode
import datetime# load confg

userCode = input('富富转账户: ')
userPass = input('富富转密码: ')
wechatGroupNumber = input('微信群总数: ')
setSuccess = 'http://sm.ewmtool.com/insertRecord?codeSuccess=0&recordId='
setError = 'http://sm.ewmtool.com/insertRecord?codeSuccess=1&recordId='
# now date time
nowDate = datetime.datetime.now().strftime("%Y-%m-%d")
nowTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%i:%s")

# Login POST
getLogin = requests.post('http://sm.ewmtool.com/getLogin', data={'userCode': userCode, 'userPass': userPass})

print(getLogin.json())

# put wechat group number
userDayCount = requests.post('http://sm.ewmtool.com/userDayCount', data={'number': wechatGroupNumber}, cookies=getLogin.cookies)

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


