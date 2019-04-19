import json
import traceback

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from LostFoundDjangoService.models import Dynamic, UserInfo


@csrf_exempt
def create(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'user_id','type','category','content'}.issubset(request.POST.keys()):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
    try:
        params = request.POST.dict()
        Dynamic.objects.create(**params)
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
        qset=Dynamic.objects.filter(**params).order_by('ctime')[page*size:(page+1)*size]
        dynamics=json.loads(serializers.serialize("json", qset))
        print(dynamics)
        for dynamic in dynamics:
            data_row=dynamic['fields']
            data_row['dynamic_id']=dynamic['pk']
            data_row['user_info'] = json.loads(serializers.serialize("json", UserInfo.objects.filter(user_id=dynamic['fields']['user_id'])))[0]['fields']
            res['data']['dynamics'].append(data_row)
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(res))