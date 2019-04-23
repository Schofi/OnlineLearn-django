# -*- coding: utf-8 -*-
# @Time    : 2019/4/19 22:01
# @Author  : Schofi
# @File    : forms.py
# @Software: PyCharm
# @contact :1390877784@qq.com
from django import forms# 用户登录表单的验证


class LoginForm(forms.Form):
    username = forms.CharField(required=True)  # 用户名不能为空
    password = forms.CharField(required=True, min_length=5)  # 密码不能为空，而且最小6位数


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)


class ForgetForm(forms.Form):
    email = forms.CharField(required=True)  # 用户名不能为空


class ModifyPwdForm(forms.Form):
    password = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)
