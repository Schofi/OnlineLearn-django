# -*- coding: utf-8 -*-
# @Time    : 2019/4/22 19:38
# @Author  : Schofi
# @File    : urls.py
# @Software: PyCharm
# @contact :1390877784@qq.com
from django.urls import path,include,re_path
from .views import OrgView, AddUserAskView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView
from .views import OrgHomeView

app_name = "organization"


urlpatterns = [
    # 课程机构列表页url
    path('list/',OrgView.as_view(),name='org_list'),
    path("add_ask/", AddUserAskView.as_view(), name="add_ask"),
    # 课程机构首页url,此处不是普通的url是因为我们必须知道是哪个机构的首页
    re_path('home/(?P<org_id>.*)/', OrgHomeView.as_view(), name="org_home"),
    re_path('course/(?P<org_id>.*)/',OrgCourseView.as_view(), name="org_course"),
    re_path('desc/(?P<org_id>.*)/', OrgDescView.as_view(), name="org_desc"),
    re_path('teacher/(?P<org_id>.*)/', OrgTeacherView.as_view(), name="org_teacher"),
    path("add_fav/", AddFavView.as_view(), name="add_fav"),
]
