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


@csrf_exempt
def create(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    if not {'user_id','type','content'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
    try:
        params = request.POST.dict()
        params['images']=json.dumps([])
        dynamic=Dynamic.objects.create(**params)
        res['data']['dynamic_id']=dynamic.id
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def update(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'dynamic_id'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
    try:
        dynamic_id = request.POST['dynamic_id']
        params = request.POST.dict()
        params.pop('dynamic_id')
        print(params)
        Dynamic.objects.filter(id=dynamic_id).update(**params)
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def delete(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'dynamic_id'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
    try:
        dynamic_id = request.POST['dynamic_id']
        Dynamic.objects.filter(id=dynamic_id).update(status=0)
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def show(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    try:
        params = request.POST.dict()
        page=0
        size=20
        if 'page' in params:
            page=params['page']
            params.pop('page')
        if 'size' in params:
            size=params['size']
            params.pop('size')
        params['status']=1
        res['data']['count']=Dynamic.objects.filter(**params).count()
        res['data']['dynamics']=[]
        qset=Dynamic.objects.filter(**params).order_by('-ctime')[page*size:(page+1)*size]
        dynamics=json.loads(serializers.serialize("json", qset))
        print(dynamics)
        for dynamic in dynamics:
            data_row=dynamic['fields']
            data_row['dynamic_id']=dynamic['pk']
            data_row['images']=json.loads(data_row['images'])
            if len(data_row['location'])>=2:
                data_row['location'] = json.loads(data_row['location'])
            else:
                data_row['location']={}
            data_row['user_info'] = json.loads(serializers.serialize("json", UserInfo.objects.filter(user_id=dynamic['fields']['user_id'])))[0]['fields']
            res['data']['dynamics'].append(data_row)
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def picRcgnz(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if request.method == 'POST':
        files = request.FILES.getlist('images', None)  # input 标签中的name值
        if not files:
            res={'code':-1,'msg':"无上传图片", 'data':[]}
        else:
            results=[]
            try:
                for file in files:
                    # client_id 为官网获取的AK， client_secret 为官网获取的SK
                    url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=r0xoXpw4o5LB3iYBGmGsiCiF&client_secret=CS25qfGwgkV6iokIfmTta5kttnerhN51'
                    headers = {'Content-Type': 'application/json; charset=UTF-8'}
                    r = requests.get(url, headers=headers)
                    access_token = r.json()['access_token']
                    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                    img = base64.b64encode(file.read())
                    request_url = request_url + "?access_token=" + access_token
                    params = {"image": img}
                    r = requests.post(request_url, data=params)
                    print(r.json())
                    results.extend(r.json()['result'])
                res['data'] = results[0]
                for r in results:
                    if r['score']>res['data']['score']:
                        res['data']=r
            except Exception as e:
                res['code']=-2
                res['msg']=e
                res['data']=[]
    return HttpResponse(json.dumps(res))