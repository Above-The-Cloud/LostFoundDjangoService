import json
import traceback

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



def studentLogin(stu_id, stu_pwd):
    try:
        url = 'http://202.120.82.2:8081/ClientWeb/pro/ajax/login.aspx'
        params = {"id":stu_id,"pwd":stu_pwd,"act":'login'}
        r=requests.post(url, data=params,timeout=5)
        print(r)
    except:
        traceback.print_exc()
        return {'ret':-1}
    return json.loads(r.text)

def getOpenid(code):
    data={
        'appid':'wxd8d5a2f6fa7f1878',
        'secret':'c1377133ab2c26acf453a0d7ed877710',
        'grant_type':'authorization_code',
        'js_code':code
    }
    url='https://api.weixin.qq.com/sns/jscode2session'
    try:
        print(data)
        r=requests.post(url,data=data)
    except:
        traceback.print_exc()
        return {'code':-1,'msg':'timeout | getopenid failed!','data':[]}
    return {'code':0, 'msg':'success','data':json.loads(r.text)}