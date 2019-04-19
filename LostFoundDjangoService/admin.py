from django.contrib import admin

from LostFoundDjangoService.models import Student, UserInfo, UserOpenid, Dynamic

class StudentAdmin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('id','stu_id','stu_pwd','status','ctime','mtime')

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','nick_name','avatar_url','contact_type','contact_value','role','status','ctime','mtime')

class UserOpenidAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','openid','status','ctime','mtime')

class DynamicAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','type','category','title','content','images','status','ctime','mtime')


admin.site.register(Student,StudentAdmin)
admin.site.register(UserInfo,UserInfoAdmin)
admin.site.register(UserOpenid,UserOpenidAdmin)
admin.site.register(Dynamic,DynamicAdmin)

# admin.site.register([Student, UserInfo, UserOpenid, Dynamic])