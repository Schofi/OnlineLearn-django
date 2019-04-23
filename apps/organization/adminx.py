# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 20:16
# @Author  : Schofi
# @File    : adminx.py
# @Software: PyCharm
# @contact :1390877784@qq.com

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['name', 'desc']  # 查询你想要的数据
    list_filter = ['name', 'desc', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city']  # 查询你想要的数据，记住尽量不要把时间放进去
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。
    # 搜索框，当课程数据量过大时，有课程指向它，会以ajax方式加载
    relfield_style = 'fk-ajax'

class TeacherAdmin(object):
    list_display = ['org','name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['org','name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']  # 查询你想要的数据，记住尽量不要把时间放进去
    list_filter = ['org','name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)