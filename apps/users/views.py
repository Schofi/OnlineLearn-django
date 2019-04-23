from django.shortcuts import render
from django.contrib.auth import authenticate, login
# from django.contrib.auth.backends import ModelBackend
from users.models import UserProfile,EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from django.shortcuts import redirect
# Create your views here.
def index(request):
    return render(request,'bookshop/index.html')

# class CustomBackend(ModelBackend):
#     def authenticate(self,request, username=None, password=None, **kwargs):
#         try:
#             user = UserProfile.objects.get(Q(username=username) | Q(email=username))
#             if user.check_password(password):
#                 return user
#         except Exception as e:
#             return None

def user_login(request):
    if request.method =='POST':
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')  # 取值成功返回user对象,失败返回null
        user = authenticate(request=request,username=user_name, password=pass_word)

        if user:  # login 有两个参数：request和user。我们在请求的时候，request实际上是写进了一部分信息，
            # 然后在render的时候，这些信息也被返回前端页面从而完成用户登录。
            login(request,user)  # 页面跳转至网站首页 user request也会被带回到首页，显示登录状态
            return render(request, "index.html")
        else:
            return render(request,"login.html",{'msg': '用户名或者密码错误！'})
    elif request.method == 'GET':
        return render(request,"login.html",{})

class LoginView(View):
    def get(self, request):
        # render的作用是渲染html并返回给用户
        # render三要素: request ，模板名称 ，一个字典用于传给前端并在页面显示
        return render(request, "login.html", {})  # 不需要判断，直接调用post方法

    def post(self, request):
        # 类的实例化需要一个字典dict参数，而前面我们就知道request.POST是一个QueryDict，所以可以直接传入POST中的username，password等信息
        login_form = LoginForm(request.POST)  # is_valid()方法，用来判断我们所填写的字段信息是否满足我们在LoginForm中所规定的要求，验证成功则继续进行，失败就跳回login页面并重新输入信息
        if login_form.is_valid():  # username，password为前端页面name的返回值，取到用户名和密码我们就开始进行登录验证;取不到时为空。
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')  # 取值成功返回user对象,失败返回null
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                # login 有两个参数：request和user。我们在请求的时候，request实际上是写进了一部分信息，然后在render的时候，这些信息也被返回前端页面从而完成用户登录
                if user.is_active:
                    login(request, user)  # 页面跳转至网站首页 user request也会被带回到首页，显示登录状态
                    return render(request, "index.html")
                else:
                    return render(request,"login.html",{"msg":"用户未激活"})

            else:
                return render(request, "login.html", {'msg': '用户名或者密码错误！', "login_form": login_form})
        else:
            return render(request, "login.html", {'msg': '用户名或者密码错误！',"login_form":login_form})

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        # render的作用是渲染html并返回给用户
        # render三要素: request ，模板名称 ，一个字典用于传给前端并在页面显示
        return render(request, "register.html", {'register_form':register_form})  # 不需要判断，直接调用post方法

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email","")
            if UserProfile.objects.filter(email=user_name):
                return render(request,"register.html",{"register_form":register_form,"msg":"用户已经存在",})
            pass_word = request.POST.get("password","")
            user_profile = UserProfile()
            user_profile.username=user_name
            user_profile.email=user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active=False
            user_profile.save()

            send_register_email(user_name,"register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {'register_form':register_form})

class ActiveUserView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
        else:
            return render(request,"active_fail.html")
        return redirect('/login/')

class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {'forget_form': forget_form})

    def post(self,request):
        forget_form=ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email,"forget")
            return render(request,"send_success.html")
        else:
            return render(request, "forgetpwd.html", {'forget_form': forget_form})

class ResetView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,"password_reset.html",{"email":email})
        else:
            return render(request,"active_fail.html")
        return redirect('/login/')

class ModifyPwdView(View):
    def post(self,request):
        modify_form =ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get("password","")
            pwd2= request.POST.get("password2","")
            email = request.POST.get("email","")
            if (pwd1 != pwd2):
                return render(request, "password_reset.html", {"email": email, "msg": "对不起，前后密码不一致"})
            else:
                user=UserProfile.objects.get(email=email)
                user.password=make_password(pwd2)
                user.save()
                return redirect('/login/')
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "msg": "对不起，前后密码不一致"})
