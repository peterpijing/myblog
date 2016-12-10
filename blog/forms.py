#coding=utf-8

from django import forms

from models import User

# class RegForm(forms.ModelForm):
#
#
#     class Meta:
#         model = User


class AddForm(forms.Form):
    a = forms.IntegerField()
    b =  forms.IntegerField()


#1.定义一个评论表单
TOPIC_CHOICES = (
    ('level1','Bad'),
    ('level2','SoSo'),
    ('level3','Good'),
)


#1.将表单模型和数据库模型做调整，以及绑定  为何label这里不支持中文？？？？
class RemarkForm(forms.Form):
    subject = forms.CharField(max_length=100, label='Mark Board')
    mail = forms.EmailField(label='email')
    topic = forms.ChoiceField(choices=TOPIC_CHOICES, label='choose one topic')
    message = forms.CharField(label='content for mark', widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False, label='watch this tie')

    # subject = forms.CharField(max_length=100, label='主题')
    # mail = forms.EmailField(label='电子邮件')
    # topic = forms.ChoiceField(choices=TOPIC_CHOICES, label='选择等级')
    # message = forms.CharField(label='内容', widget=forms.Textarea)
    # cc_myself = forms.BooleanField(required=False, label='关注')


#2.定义图片上传表单－－根据model中的图片上传模型
class NormalUserForm(forms.Form):
    username = forms.CharField()
    headImg = forms.FileField()