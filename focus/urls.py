from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$',index,name='index'),
    url(r'^login/$', log_in, name='login'),
    url(r'^logout/$', log_out, name='logout'),
    url(r'^(?P<article_id>[0-9]+)/$', article, name='article'),
    url(r'^(?P<article_id>[0-9]+)/comment/$', comment, name='comment'),
    url(r'^(?P<article_id>[0-9]+)/keep/$',get_keep,name='keep'),
    url(r'^(?P<article_id>[0-9]+)/poll/$', get_poll_article, name='poll'),

    url(r'^addarticle/$',addarticle,name='addarticle'),
    url(r'^changepwd/$',changepwd,name='changepwd'),
    url(r'register/$',register,name='register'),

]