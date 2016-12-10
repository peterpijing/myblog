#coding=utf-8
from django import template


#1.自定义过滤器
register = template.Library()

def month_to_upper(key):
    return ['一','二','三','四','五','六','七','八','九','十','十一','十二'][key-1]


#注册过滤器
register.filter('month_to_upper',month_to_upper)