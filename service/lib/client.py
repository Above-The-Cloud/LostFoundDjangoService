import json
import traceback

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



def studentLogin(stu_id, stu_pwd):
    try:
        url = 'http://202.120.82.2:8081/ClientWeb/pro/ajax/login.aspx'
        params = {"id":stu_id,"pwd":stu_pwd,"act":'login'}
        r=requests.post(url, data=params)
        print(r)
    except:
        traceback.print_exc()
    return json.loads(r.text)