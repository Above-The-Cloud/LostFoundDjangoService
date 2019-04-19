import traceback

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from LostFoundDjangoService.models import UserInfo, Student

@csrf_exempt
def import_user(request):
    try:
        f=open("user/script/user.csv",encoding='UTF-8')
        for i,line in enumerate(f):
            print(i)
            user=line.split(',')
            Student.objects.create(stu_id=int(user[0]), stu_pwd=user[1])
            UserInfo.objects.create(user_id=int(user[0]),nick_name=user[2],avatar_url='https://lostandfound.yiwangchunyu.wang/meida/system/ecnu_avatar.gif')
        print('done!')
    except:
        traceback.print_exc()
    return HttpResponse('done')