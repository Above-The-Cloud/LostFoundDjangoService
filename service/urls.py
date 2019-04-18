
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from service.lib import client
from . import views

urlpatterns = [
    url(r'^$', views.hello),
    url(r'^loginByOpenid$', views.loginByOpenid),
    url(r'^loginByUid$', views.loginByUid),
    url(r'^studentLogin$', views.studentLogin),

]
