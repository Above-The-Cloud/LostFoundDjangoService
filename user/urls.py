
from django.conf.urls import url
from django.urls import include

from user.script import import_user
from . import views

urlpatterns = [
    url(r'^loginByOpenid$', views.loginByOpenid),
    url(r'^loginByUid$', views.loginByUid),
    url(r'^studentLogin$', views.studentLogin),
    url(r'^logout$', views.logout),
    url(r'^getById$', views.getById),
    url(r'^update$', views.update),
    # url(r'^import_user$', import_user.import_user),

]
