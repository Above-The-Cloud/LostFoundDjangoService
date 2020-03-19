from django.shortcuts import render

# Create your views here.
import base64
import json
import traceback

import requests
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from LostFoundDjangoService.models import Dynamic, UserInfo
from lib.sms import send
from notify.models import Notify


# @csrf_exempt
# def create(request):
#     res = {'code': 0, 'msg': 'success', 'data': {}}
#     if not {'user_id','dynamic_id'}.issubset(request.POST.keys()):
#         return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
#     try:
#         params = request.POST.dict()
#         notify_id=Notify.objects.create(**params)
#         res['data']['notify_id']=notify_id.id
#         dynamic=Dynamic.objects.get(id=params['dynamic_id'])
#         if  dynamic.type=='found' and dynamic.category=='校园卡':
#             user=UserInfo.objects.get(user_id=dynamic.user_id)
#             if user.contact_type=='手机号':
#                 send(user.contact_value, user.nick_name, '校园卡')
#     except:
#         traceback.print_exc()
#     return HttpResponse(json.dumps(res))

@csrf_exempt
def update(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'notify_id'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
    try:
        notify_id = request.POST['notify_id']
        params = request.POST.dict()
        params.pop('notify_id')
        Notify.objects.filter(id=notify_id).update(**params)

    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(res))


@csrf_exempt
def list(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    if not {'user_id'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
    try:
        params = request.POST.dict()
        page=0
        size=40
        if 'page' in params:
            page=params['page']
            params.pop('page')
        if 'size' in params:
            size=params['size']
            params.pop('size')
        params['status']=1
        res['data']['count']=Notify.objects.filter(**params).count()
        res['data']['notify']=[]
        qset=Notify.objects.filter(**params).order_by('-ctime')[page*size:(page+1)*size]
        notifys=json.loads(serializers.serialize("json", qset))
        res['data']['count']=len(notifys)
        res['data']['notifys'] = []
        for i in range(len(notifys)):
            url='https://lostandfound.yiwangchunyu.wang/service/dynamic/show'
            # url = 'http://127.0.0.1:8000/service/dynamic/show'
            data={'id':notifys[i]['fields']['dynamic_id']}
            r = requests.post(url=url,data=data)
            d = r.json()
            res['data']['notifys'].append(d['data']['dynamics'][0])
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

