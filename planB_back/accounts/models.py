from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager


class Province(models.Model):
    name = models.CharField('نام استان', max_length=20, unique=True)
    code = models.CharField('کد استان', max_length=10, unique=True)

    class Meta:
        ordering = ['code']
        verbose_name_plural = 'استان ها'
        verbose_name = 'استان'

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, verbose_name='شهر', on_delete=models.PROTECT)
    name = models.CharField('نام شهر', max_length=20, unique=True)
    code = models.CharField('کد شهر', max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']
        verbose_name_plural = 'شهر ها'
        verbose_name = 'شهر'
        unique_together = ('name', 'province',)


class University(models.Model):
    city = models.ForeignKey(City, verbose_name='شهر', on_delete=models.PROTECT)
    name = models.CharField('نام دانشگاه', max_length=20)
    code = models.CharField('کد دانشگاه', max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']
        verbose_name_plural = "دانشگاه ها"
        verbose_name = "دانشگاه"
        unique_together = ('name', 'city',)


class Skill(models.Model):
    name = models.CharField('نام مهارت', max_length=30, unique=True)
    code = models.CharField('کد مهارت', max_length=10, unique=True)
    skill = models.ForeignKey('self', verbose_name='پدر مهارت', on_delete=models.PROTECT, related_name='child_skill',
                              null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']
        verbose_name_plural = "مهارت ها"
        verbose_name = "مهارت"


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('MALE', 'مرد'),
        ('FEMALE', 'زن'),
    )
    username = models.CharField('نام کاربری', max_length=30, unique=True)
    password = models.CharField('رمز عبور', max_length=128)
    email = models.EmailField('ایمیل', max_length=254, unique=True)
    phone_number = PhoneNumberField('شماره تلفن', null=True, blank=True, unique=True)
    first_name = models.CharField('نام', max_length=30)
    last_name = models.CharField('نام خانوادگی', max_length=30)
    gender = models.CharField('جنسیت', max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    avatar = models.ImageField('عکس', null=True, blank=True, upload_to='avatars/')
    is_active = models.BooleanField('فعال', default=True)
    is_admin = models.BooleanField('کاربر خاص', default=False)
    date_joined = models.DateTimeField('تاریخ عضویت', auto_now_add=True)
    description = models.TextField('توضیحات', null=True, blank=True, max_length=200)
    university = models.ForeignKey(University, verbose_name='نام دانشگاه', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    city = models.ForeignKey(City, verbose_name='شهر', on_delete=models.SET_NULL, null=True, blank=True)
    skills = models.ManyToManyField(Skill, verbose_name='مهارت ها', blank=True)

    class Meta:
        ordering = ['username']
        verbose_name_plural = "کاربران"
        verbose_name = "کاربر"

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', ]

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Project(models.Model):
    SITUATION_CHOICES = (
        ('WAITING', 'در حال انتظار'),
        ('STARTED', 'شروع شده'),
        ('ENDED', 'پایان یافته'),
    )
    # project_owner_id = models.ForeignKey(User,verbose_name='کارفرما' ,on_delete=models.PROTECT)
    name = models.CharField('نام پروژه', max_length=30)
    skills = models.ManyToManyField(Skill, verbose_name='مهارت ها')
    creator = models.ManyToManyField(User, through='User_Project', verbose_name='اعضا', blank=True)
    description = models.TextField('توضیحات', null=True, blank=True, max_length=200)
    create_date = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    situation = models.CharField('وضعیت پروژه', max_length=7, choices=SITUATION_CHOICES)
    duration = models.DurationField('مدت زمان')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "پروژه ها"
        verbose_name = "پروژه"


class User_Project(models.Model):
    SITUATION_CHOICES = (
        ('ACCEPTED', 'پذیرفته شده'),
        ('REQUESTED', 'درخواست داده شده'),
        ('DECLINED', 'رد شده'),
    )
    project = models.ForeignKey(Project, verbose_name='پروژه', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
    situation = models.CharField(max_length=9, verbose_name='وضعیت', choices=SITUATION_CHOICES)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "پروژه ها"
        verbose_name = "پروژه"


class Temp(models.Model):
    email = models.EmailField(verbose_name="ایمیل", validators=[validate_email], max_length=255)
    date = models.DateTimeField(verbose_name="تاریخ", auto_now=True)
    code = models.CharField(verbose_name="کد", max_length=20)

    class Meta:
        ordering = ['date']
        verbose_name = "میانی"
        verbose_name_plural = "میانی ها"
