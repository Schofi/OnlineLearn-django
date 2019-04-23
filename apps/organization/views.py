from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from operation.models import UserFavorite
from .models import CityDict, CourseOrg
# Create your views here.
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.forms import AnotherUserAskForm  # 我要学习功能实现


class OrgView(View):
    def get(self, request):
        all_citys = CityDict.objects.all()  # 查找所有的课程机构信息
        all_orgs = CourseOrg.objects.all()
        # 对课程机构进行分页,尝试获取前端get请求传递过来的page参数
        # city,pgae相当于他已经做好了的页面关键值，city传入参数是为了做刷选,request.get是以字符键值对传递的
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        city_id = request.GET.get("city", "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 选中了类别之后，根据category与数据库中的category进行判断，从而显示授课机构
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        org_nums = all_orgs.count()

        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html",
                      {
                          "all_citys": all_citys,
                          "all_orgs": orgs,
                          "org_nums": org_nums,
                          "city_id": city_id,
                          "category": category,
                          "hot_orgs": hot_orgs,
                          "sort": sort
                      })


class AddUserAskView(View):
    def post(self, request):
        userask_form = AnotherUserAskForm(request.POST)  # 判断form是否有效
        if userask_form.is_valid():
            #  注意modelform和form的区别，modelform它有model的属性，而且有个参数commit，当它为真时会把数据存入到数据库
            user_ask = userask_form.save(commit=True)
            # 如果保存成功,则返回json,不过后面必须有content_type用于告诉浏览器返回的类型
            return HttpResponse(
                "{'status': 'success'}",
                content_type='application/json')
        else:
            # 如果保存失败，则返回json,并将form的错误信息通过msg传递到前端进行显示
            return HttpResponse(
                "{'status':'fail','msg':{'登陆报错'}}",
                content_type='application/json')


# 机构首页
class OrgHomeView(View):
    def get(self, request, org_id):
        # 根据id来获取课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 根据取到的课程机构直接获取它的所有课程，我们取3个
        all_courses = course_org.course_set.all()[:3]
        # 根据取到的课程机构直接获取它的所有讲师，我们取1个
        all_teachers = course_org.teacher_set.all()[:1]
        current_page = "home"
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,
                      "org-detail-homepage.html",
                      {"current_page": current_page,
                       "all_courses": all_courses,
                       "all_teachers": all_teachers,
                       "course_org": course_org,
                       "has_fav": has_fav})


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = "course"
        # 根据id来获取课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 根据取到的课程机构直接获取它的所有课程，我们取3个
        all_courses = course_org.course_set.all()
        # 根据取到的课程机构直接获取它的所有讲师，我们取1个
        all_teachers = course_org.teacher_set.all()[:1]
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,
                      "org-detail-course.html",
                      {"current_page": current_page,
                       "all_courses": all_courses,
                       "all_teachers": all_teachers,
                       "course_org": course_org,
                       "has_fav": has_fav})


# 机构课程详情页
class OrgDescView(View):
    def get(self, request, org_id):
        current_page = "desc"
        # 根据id来获取课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, "org-detail-desc.html",
                      {
                          "course_org": course_org,
                          "current_page": current_page,
                          "has_fav": has_fav
                      })


# 机构讲师列表页
class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "teachers"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, "org-detail-teachers.html",
                      {
                          "course_org": course_org,
                          "current_page": current_page,
                          "all_teachers": all_teachers,
                          "has_fav": has_fav
                      })


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)  # 这是课程机构的id尽管我们取出的是字符串，但是后面会进行整型转换，空字符串转换会出错
        fav_type = request.POST.get('fav_type', 0)
        # 判断用户是否登录，即使没登录也会有一个匿名的user
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，那我们删除它就表示用户取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            # 记录不存在，那我们就添加一条数据进入数据库里面
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.user = request.user
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')