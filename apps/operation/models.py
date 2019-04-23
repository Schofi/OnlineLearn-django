from django.db import models
from datetime import datetime
from users.models import UserProfile
from courses.models import Course
# Create your models here.
#1、用户提交我要学习的个人需求记录；
#2、用户的课程评论信息记录；
#3、用户用于收藏公开课, 授课讲师, 授课机构以及用户消息提醒的记录；
#4、用户个人中心里面我的课程说明，用户和课程之间的学习信息记录
#5、用户咨询消息的记录等.



# 用户我要学习信息
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 课程评论
class CourseComments(models.Model):
    # 前面知道一个用户发表多个课程评论，所以在课程评论表中将用户设置为外键。
    # 此处的user其实就是一个用来告诉我们这个课程评论属于哪个用户的字段
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户名")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    comment = models.CharField(max_length=200, verbose_name="评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment

# 用户收藏信息
class UserFavorite(models.Model):
    # 前面知道一个用户可以收藏多个内容，所以在用户收藏表中将用户设置为外键。
    # 此处的user其实就是一个用来告诉我们这个用户收藏属于哪个用户的字段
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户名")
    fav_id = models.IntegerField(default=0, verbose_name='数据Id')
    fav_type = models.CharField(choices=(('1', '课程'), ('2', '课程机构'), ('3', '讲师')), default=1,verbose_name='收藏类型', max_length=2)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user

# 用户消息信息
class UserMessage(models.Model):

    user = models.IntegerField(default=0, verbose_name="接收用户")
    message = models.CharField(max_length=500, verbose_name='消息内容')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


# 用户课程信息
class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户名')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='学习时间')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


