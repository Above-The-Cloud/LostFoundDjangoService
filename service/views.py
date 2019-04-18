import json
import traceback

from django.core import serializers
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from LostFoundDjangoService.models import UserOpenid, Student, UserInfo
from service.lib import client


def hello(request):
    return HttpResponse("Hello world ! ")

def loginByOpenid(request):
    res={'code':0, 'msg':'success', 'data':[]}
    try:
        openid=request.GET['openid']
        qset=UserOpenid.objects.filter(openid=openid, status=1)
        if len(qset)==1:
            res={'code':0, 'msg':'success', 'data':json.loads(serializers.serialize("json", qset))}
        else:
            res={'code':-1, 'msg':'user auto login failed!', 'data':[]}
    except:
        traceback.print_exc()
    print(res)
    return HttpResponse(json.dumps(res))

def loginByUid(request):
    res={'code':0, 'msg':'success', 'data':[]}
    if  not {'user_id','password','openid','avatar_url'}.issubset(set(request.GET.keys())):
        return HttpResponse(json.dumps({'code':-3,'msg':'unexpected params!', 'data':[]}))
    try:
        user_id=request.GET['user_id'].strip()
        password=request.GET['password'].strip()
        openid = request.GET['openid'].strip()
        avatar_url = request.GET['avatar_url'].strip()
        print(user_id[:2])
        if user_id[:2]=='78': #楼宇管理员
            qset = Student.objects.filter(stu_id=user_id, stu_pwd=password)
            if len(qset)==1:
                res = {'code': 0, 'msg': 'success', 'data': json.loads(serializers.serialize("json", qset))}
                if(UserOpenid.objects.filter(openid=openid,user_id=user_id).count())>0:
                    UserOpenid.objects.filter(openid=openid, user_id=user_id).update(status=1)
                else:
                    UserOpenid.objects.create(openid=openid,user_id=user_id)
            else:
                res={'code': -2, 'msg': '用户名或密码不正确!', 'data': []}
        else:
            user_info=client.studentLogin(user_id,password)
            if user_info['ret']==1:
                res = {'code': 0, 'msg': 'success', 'data': user_info['data']}
                if (UserOpenid.objects.filter(openid=openid, user_id=user_id).count()) > 0:
                    UserOpenid.objects.filter(openid=openid, user_id=user_id).update(status=1)
                else:
                    UserOpenid.objects.create(openid=openid, user_id=user_id)

                if (UserInfo.objects.filter(user_id=user_id).count()) == 0:
                    UserInfo.objects.create(user_id=user_id,nick_name=user_info['data']['name'],role=2,avatar_url=avatar_url)
                else:
                    UserInfo.objects.filter(user_id=user_id).update(avatar_url=avatar_url)
            elif user_info['ret']==0:
                res = {'code': -2, 'msg': '用户名或密码不正确', 'data': []}
            else:
                res = {'code': -3, 'msg': '校园网络管制！', 'data': []}
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def studentLogin(request):
    return HttpResponse(client.studentLogin(request.POST['stu_id'],request.POST['stu_pwd']))