# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 20:11
# @Author  : Schofi
# @File    : adminx.py
# @Software: PyCharm
# @contact :1390877784@qq.com

import xadmin
from .models import UserAsk,CourseComments,UserFavorite,UserMessage,UserCourse

class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name', 'add_time']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']



class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comment', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['user', 'course', 'comment']  # 查询你想要的数据，记住尽量不要把时间放进去
    list_filter = ['user', 'course', 'comment', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['user', 'fav_id', 'fav_type']  # 查询你想要的数据，记住尽量不要把时间放进去
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['user', 'message', 'has_read']  # 查询你想要的数据，记住尽量不要把时间放进去
    list_filter = ['user', 'message', 'has_read', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


class UserCourseAdmin(object):
    list_display = ['user',  'course', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['user',  'course']  # 查询你想要的数据，记住尽量不要把时间放进去
    list_filter = ['user',  'course', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)


