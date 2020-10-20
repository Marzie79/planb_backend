from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import validate_email
from accounts.managers import UserManager


class User(AbstractBaseUser):
    username = models.CharField("نام کاربری", max_length=30, unique=True)
    first_name = models.CharField("نام", max_length=30)
    last_name = models.CharField("نام خانوادگی", max_length=30)
    password = models.CharField("رمز", max_length=128)
    email = models.EmailField("ایمیل", validators=[validate_email], max_length=255, unique=True)
    is_active = models.BooleanField(verbose_name="فعال", default=True)
    is_admin = models.BooleanField(verbose_name="ادمین", default=False)

    class Meta:
        ordering = ['last_name']
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

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


class Temp(models.Model):
    email = models.EmailField(verbose_name="ایمیل", validators=[validate_email], max_length=255)
    date = models.DateTimeField(verbose_name="تاریخ", auto_now=True)
    code = models.CharField(verbose_name="کد", max_length=20)

    class Meta:
        ordering = ['date']
        verbose_name = "میانی"
        verbose_name_plural = "میانی ها"
