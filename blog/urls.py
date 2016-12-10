from django.conf.urls import url

from views import *

urlpatterns = [
    # url(r'^$',index,name='index'),
    url(r'^add/$',add,name='add'),
    url(r'^remark/$',remark,name='remark'),

    # upload images
    url(r'^register/$',registerNormalUser,name='register'),
]