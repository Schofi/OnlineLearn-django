# -*- coding: utf-8 -*-
# @Time    : 2019/4/20 12:31
# @Author  : Schofi
# @File    : email_send.py
# @Software: PyCharm
# @contact :1390877784@qq.com
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from random import Random
from learnj.settings import EMAIL_FROM



def send_register_email(email,send_type="register"):
    email_record = EmailVerifyRecord()
    code=random_str(16)
    email_record.code=code
    email_record.email=email
    email_record.send_type=send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type =="register":
        email_title = "欢迎你注册"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}/".format(code)
        # 使用Django内置的函数来完成邮件的发送        ，包括四个参数：主题，邮件内容，从哪里发，接收者list
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = '重置密码链接'
        email_body="请点击下面的链接重置你的账号: http://127.0.0.1:8000/reset/{0}/".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass



def random_str(randomlength=8):
    str=''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

