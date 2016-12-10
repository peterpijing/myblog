from django.contrib import admin

# Register your models here.

from models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email', 'create_date')
    list_filter = ['create_date']
    search_fields = ['username']


admin.site.register(User,UserAdmin)