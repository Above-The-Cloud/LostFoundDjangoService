import json
import os
import random
import time
import traceback

import requests
from django.core import serializers

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from LostFoundDjangoService import settings
from LostFoundDjangoService.models import UserOpenid, Student, UserInfo
from LostFoundDjangoService.settings import MEDIA_URL_PREFIX
from lib import client


def hello(request):
    return HttpResponse("Hello world ! ")

@csrf_exempt
def loginByOpenid(request):
    res={'code':0, 'msg':'success', 'data':[]}
    try:
        openid=request.POST['openid']
        qset=UserOpenid.objects.filter(openid=openid, status=1)
        if len(qset)==1:
            res={'code':0, 'msg':'success', 'data':json.loads(serializers.serialize("json", qset))[0]['fields']}
        else:
            res={'code':-1, 'msg':'user auto login failed!', 'data':[]}
    except:
        traceback.print_exc()
    print(res)
    return HttpResponse(json.dumps(res))

@csrf_exempt
def loginByUid(request):
    res={'code':-4, 'msg':'fail', 'data':[]}
    if  not {'user_id','password','openid','avatar_url'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-3,'msg':'unexpected params!', 'data':[]}))
    try:
        user_id=request.POST['user_id'].strip()
        password=request.POST['password'].strip()
        openid = request.POST['openid'].strip()
        avatar_url = request.POST['avatar_url'].strip()
        print(user_id[:2])
        if user_id[:2]=='78': #楼宇管理员
            qset = Student.objects.filter(stu_id=user_id, stu_pwd=password)
            if len(qset)==1:
                res = {'code': 0, 'msg': 'success', 'data': json.loads(serializers.serialize("json", UserInfo.objects.filter(user_id=user_id)))[0]['fields']}
                if(UserOpenid.objects.filter(openid=openid,user_id=user_id).count())>0:
                    UserOpenid.objects.filter(openid=openid, user_id=user_id).update(status=1)
                else:
                    UserOpenid.objects.create(openid=openid,user_id=user_id)
            else:
                res={'code': -2, 'msg': '用户名或密码不正确!', 'data': []}
        else:
            user_info= client.studentLogin(user_id, password)
            if user_info['ret']==1:
                res = {'code': 0, 'msg': 'success', 'data': user_info['data']}
                if (UserOpenid.objects.filter(openid=openid, user_id=user_id).count()) > 0:
                    UserOpenid.objects.filter(openid=openid, user_id=user_id).update(status=1)
                else:
                    UserOpenid.objects.create(openid=openid, user_id=user_id)

                if (UserInfo.objects.filter(user_id=user_id).count()) == 0:
                    r = requests.get(avatar_url)
                    date = time.strftime('%Y%m%d', time.localtime())
                    dirs = settings.MEDIA_ROOT + '/avatar/' + date + '/'
                    url_mid = '/media/avatar/' + date + '/'
                    fname = 'avatar_' + str(int(round(time.time() * 1000))) + '_' + str(random.randint(0, 10000)) + 'jpg'
                    folder = os.path.exists(dirs)
                    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                        os.makedirs(dirs)
                    with open(dirs+fname, "wb") as code:
                        code.write(r.content)

                    UserInfo.objects.create(user_id=user_id,nick_name=user_info['data']['name'],role=2,avatar_url=MEDIA_URL_PREFIX+url_mid+fname)
                    res = {'code': 0, 'msg': 'success', 'data': json.loads(serializers.serialize("json", UserInfo.objects.filter(user_id=user_id)))[0]['fields']}

                else:
                    UserInfo.objects.filter(user_id=user_id).update(avatar_url=avatar_url)
            elif user_info['ret']==0:
                res = {'code': -2, 'msg': '用户名或密码不正确', 'data': []}
            else:
                res = {'code': -3, 'msg': '网络错误！', 'data': []}
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def studentLogin(request):
    return HttpResponse(client.studentLogin(request.POST['stu_id'], request.POST['stu_pwd']))

@csrf_exempt
def logout(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'user_id','openid'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -3, 'msg': 'unexpected params!', 'data': []}))
    try:
        user_id = request.POST['user_id'].strip()
        openid = request.POST['openid'].strip()
        if (UserOpenid.objects.filter(openid=openid, user_id=user_id).count()) > 0:
            UserOpenid.objects.filter(openid=openid, user_id=user_id).update(status=0)
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def getById(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'user_id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -3, 'msg': 'unexpected params!', 'data': []}))
    try:
        user_id = request.POST['user_id'].strip()
        res['data']=json.loads(serializers.serialize("json", UserInfo.objects.filter(user_id=user_id)))[0]['fields']
        print(res)

    except:
        traceback.print_exc()

    return HttpResponse(json.dumps(res))

@csrf_exempt
def update(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'user_id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -3, 'msg': 'unexpected params!', 'data': []}))
    try:
        user_id = request.POST['user_id'].strip()
        # print(request.GET)
        params=request.POST.dict()
        # print(params)
        params.pop('user_id')
        # print(params)
        UserInfo.objects.filter(user_id=user_id).update(**params)

    except:
        traceback.print_exc()

    return HttpResponse(json.dumps(res))

@csrf_exempt
def getOpenid(request):
    if not {'js_code'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -3, 'msg': 'unexpected params!', 'data': request.POST.dict()}))
    res=client.getOpenid(request.POST['js_code'])
    return HttpResponse(json.dumps(res))