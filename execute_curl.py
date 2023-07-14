#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/2/13 15:15
# @Author : LiuXiu

import requests   # requests模块需要使用 pip 命令安装
headers = {
    'cache-control': 'no-cache',
    'content-type': 'application/json',
}
data = '{\t"appId": appId,\t"appSecret": "appSecret"}'
response = requests.post('https://open.workec.com/auth/accesstoken', headers=headers, data=data)
