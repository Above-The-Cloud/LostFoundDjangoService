import json
import os
import random
import time

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from LostFoundDjangoService import settings

from LostFoundDjangoService.settings import MEDIA_URL_PREFIX


@csrf_exempt
def uploadImg(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if request.method == 'POST':
        files = request.FILES.getlist('images', None)  # input 标签中的name值
        if not files:
            res={'code':-1,'msg':"无上传图片", 'data':[]}
        else:
            date=time.strftime('%Y%m%d',time.localtime())
            dirs = settings.MEDIA_ROOT + '/images/'+date+'/'
            url_mid = '/media/images/'+date+'/'
            folder = os.path.exists(dirs)
            if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(dirs)  # makedirs 创建文件时如果路径不存在会创建这个路径
            try:
                for file in files:
                    t = time.time()     #PS：注释中的是上传文件中的另一种方法哦。各自选用
                    fname = file.name
                    suffix = os.path.splitext(file.name)[1]
                    fname = 'dynamic_' + str(int(round(t * 1000))) + '_' + str(random.randint(0,10000)) + suffix
                    path = dirs + fname
                    f = open(path,'wb')
                    for line in file.chunks():
                        f.write(line)
                    f.close()
                    res['data'].append(MEDIA_URL_PREFIX+url_mid+fname)
            except Exception as e:
                res['code']=-2
                res['msg']=e
            res['data']=json.dumps(res['data'])
    return HttpResponse(json.dumps(res))