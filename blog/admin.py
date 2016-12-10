#coding=utf-8
from django.contrib import admin

# Register your models here.

from models import *

class ArticleAdmin(admin.ModelAdmin):
    # fields = ('title','desc','content',)

    # list_editable = ('click_count',)

    fieldsets = (
        (None,{
            'fields':('title','desc','content')
        }),
        ('高级设置',{
            'classes':('collapse',),
            'fields':('click_count','is_recommend',)
        }),
    )

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)

admin.site.register(Remark)




