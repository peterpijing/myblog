#coding=utf-8
from django import forms

class LoginForm(forms.Form):
	uid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'id':'uid', 'placeholder': 'Username'}))
	pwd = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control' ,'id':'pwd', 'placeholder': 'Password'}))

class CommmentForm(forms.Form):
	comment = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': '80', 'rows': '6'}))

class ArticleForm(forms.Form):
	# column = forms.ForeignKey(Column, blank=True, null=True, verbose_name='belong to')
	title = forms.CharField(max_length=256)
	author = forms.IntegerField()
	# user = models.ManyToManyField('UserProfile', blank=True)
	content = forms.CharField()
	# pub_date = forms.DateTimeField()
	# update_time = forms.DateTimeField()
	# published = forms.BooleanField(default=True)
	# poll_num = forms.IntegerField(default=0)
	# comment_num = forms.IntegerField(default=0)
	# keep_num = forms.IntegerField(default=0)

	# id = forms.IntegerField()


class ChangepwdForm(forms.Form):
	oldpassword = forms.CharField(
		required = True,
		label=u"原密码",
		error_messages={'required': u'请输入原密码'},
		widget=forms.PasswordInput(
			attrs={
				'placeholder': u"请输入原密码",
			}
		),
	)

	newpassword1 = forms.CharField(
		required=True,
		label=u"新密码",
		error_messages={'required': u'请输入新密码'},
		widget=forms.PasswordInput(
			attrs={
				'placeholder': u"请输入新密码",
			}
		),
	)

	newpassword2 = forms.CharField(
		required=True,
		label=u"确认密码",
		error_messages={'required': u'请再次输入新密码'},
		widget=forms.PasswordInput(
			attrs={
				'placeholder': u"请确认密码",
			}
		),
	)

	def clean(self):
		if not self.is_valid():
			raise forms.ValidationError(u"所有项都为必填项")
		elif self.cleaned_data['newpassword1'] <> self.cleaned_data['newpassword2']:
			raise forms.ValidationError(u"两次输入的新密码不一样")
		else:
			cleaned_data = super(ChangepwdForm, self).clean()
		return cleaned_data

class RegisterForm(forms.Form):
	username = forms.CharField(label='username', max_length=100,
							   widget=forms.TextInput(attrs={'id': 'username', 'onblur': 'authentication()'}))
	email = forms.EmailField()
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)