import xadmin
from .models import EmailVerifyRecord
from .models import Banner
from xadmin import views

from users.models import EmailVerifyRecord, Banner, UserProfile
from courses.models import Course, CourseResource, Lesson, Video
from organization.models import CourseOrg, CityDict, Teacher
from operation.models import CourseComments, UserMessage, UserFavorite, UserCourse, UserAsk
from django.contrib.auth.models import Group, Permission



class EmailVerifyRecordAdmin(object):
    # 配置后台显示的列信息
    list_display = ['code', 'email', 'send_type', 'send_time']  # 一次显示你想出现的多行数据
    search_fields = ['code', 'email', 'send_type']  # 查询你想要的数据
    list_filter = ['code', 'email', 'send_type', 'send_time']  # 过滤器
    model_icon = 'fa fa-user'

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']# 一次显示你想出现的多行数据
    search_fields = ['title', 'image', 'url', 'index']  # 查询你想要的数据
    list_filter = ['title', 'image', 'url', 'index', 'add_time']  # 过滤器

xadmin.site.register(Banner, BannerAdmin)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    site_title = '我的后台管理系统'  # 站点标题
    site_footer = '我的后台'  # 站点尾注
    menu_style = 'accordion'  # 折叠收起菜单,将站点标题与站点尾注进





xadmin.site.register(views.CommAdminView, GlobalSettings)


