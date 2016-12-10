from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^accounts/login/$',login,name='index'),

]