from django.contrib import admin

from LostFoundDjangoService.models import Student, UserInfo, UserOpenid, Dynamic

class StudentAdmin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('id','stu_id','stu_pwd','status','ctime','mtime')
    search_fields = ('id','stu_id','stu_pwd','status','ctime','mtime')

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','nick_name','avatar_url','contact_type','contact_value','role','status','ctime','mtime')
    search_fields = ('id','user_id','nick_name','avatar_url','contact_type','contact_value','role','status','ctime','mtime')


class UserOpenidAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','openid','status','ctime','mtime')
    search_fields = ('id','user_id','openid','status','ctime','mtime')

class DynamicAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','type','category','content','location','status','ctime','mtime')
    search_fields = ('id','user_id','type','category','content','location','status','ctime','mtime')


admin.site.register(Student,StudentAdmin)
admin.site.register(UserInfo,UserInfoAdmin)
admin.site.register(UserOpenid,UserOpenidAdmin)
admin.site.register(Dynamic,DynamicAdmin)


# 页面标题
admin.site.site_title="ECNU LostFound"
# 登录页导航条和首页导航条标题
admin.site.site_header="ECNU LostFound Administration"
# 主页标题
admin.site.index_title="Welcome, you can manage the backstage now!"

# admin.site.register([Student, UserInfo, UserOpenid, Dynamic])