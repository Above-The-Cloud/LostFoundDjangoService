
from django.conf.urls import url
from django.urls import include

from . import views

urlpatterns = [
    url(r'^$', views.hello),
    url(r'^user/', include('user.urls')),
    url(r'^dynamic/', include('dynamic.urls')),
    url(r'^upload/', include('upload.urls')),
    url(r'^loginByOpenid$', views.loginByOpenid),
    url(r'^loginByUid$', views.loginByUid),
    url(r'^studentLogin$', views.studentLogin),
    url(r'^logout$', views.logout),
    url(r'^getById$', views.getById),

]
