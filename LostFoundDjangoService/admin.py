from django.contrib import admin

from LostFoundDjangoService.models import Student, UserInfo, UserOpenid, Dynamic

admin.site.register([Student, UserInfo, UserOpenid, Dynamic])