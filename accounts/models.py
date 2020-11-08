from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager
import jdatetime
from django.utils.translation import gettext_lazy as _


class Province(models.Model):
    name = models.CharField(_("Province_name"), max_length=20, unique=True)
    code = models.CharField(_("Province_code"), max_length=10, unique=True)

    class Meta:
        ordering = ['code']
        verbose_name_plural = _("Province")
        verbose_name = _("Province")

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, verbose_name=_("Province"), on_delete=models.PROTECT)
    name = models.CharField(_("City_name"), max_length=20, unique=True)
    code = models.CharField(_("City_Code"), max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']
        verbose_name_plural = _("City")
        verbose_name = _("City")
        unique_together = ('name', 'province',)


class University(models.Model):
    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.PROTECT)
    name = models.CharField(_("University_name"), max_length=20)
    code = models.CharField(_("University_code"), max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']
        verbose_name_plural = _("University")
        verbose_name = _("University")
        unique_together = ('name', 'city',)


class Skill(models.Model):
    name = models.CharField(_("Skill_name"), max_length=30, unique=True)
    code = models.CharField(_("Skill_code"), max_length=10, unique=True)
    skill = models.ForeignKey('self', verbose_name='پدر مهارت', on_delete=models.PROTECT, related_name='child_skill',
                              null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code']
        verbose_name_plural = _("Skill")
        verbose_name = _("Skill")


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('MALE', _("male")),
        ('FEMALE', _("female")),
    )
    username = models.CharField(_("Username"), max_length=30, unique=True)
    password = models.CharField(_("Password"), max_length=128)
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    phone_number = PhoneNumberField(_("Phone_Number"), null=True, blank=True, unique=True)
    first_name = models.CharField(_("First_Name"), max_length=30)
    last_name = models.CharField(_("Last_Name"), max_length=30)
    gender = models.CharField(_("Gender"), max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    avatar = models.ImageField(_("Avatar"), null=True, blank=True, upload_to='avatars/')
    is_active = models.BooleanField(_("is_active"), default=True)
    #is_superuser is already used into AbstractBaseUser and only i override it instead of create otherfield
    is_superuser = models.BooleanField(_("is_superuser"), default=False)
    date_joined = models.DateTimeField(_("Date_joined"), auto_now_add=True)
    description = models.TextField(_("Description"), null=True, blank=True, max_length=200)
    university = models.ForeignKey(University, verbose_name=_("University_Name"), on_delete=models.SET_NULL, null=True,
                                   blank=True)
    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.SET_NULL, null=True, blank=True)
    skills = models.ManyToManyField(Skill, verbose_name=_("Skill"), blank=True)

    class Meta:
        ordering = ['username']
        verbose_name_plural = _("Users")
        verbose_name = _("Users")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', ]

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def date_joined_decorated(self):
        return jdatetime.datetime.fromgregorian(datetime=self.date_joined).strftime("%a, %d %b %Y %H:%M:%S")

    date_joined_decorated.short_description = _("date_join_decorated")

    @property
    def is_staff(self):
        return self.is_superuser


class Project(models.Model):
    SITUATION_CHOICES = (
        ('WAITING', _("Waiting")),
        ('STARTED', _("Started")),
        ('ENDED', _("Ended")),
    )
    # project_owner_id = models.ForeignKey(User,verbose_name='کارفرما' ,on_delete=models.PROTECT)
    name = models.CharField(_("Project_Name"), max_length=30)
    skills = models.ManyToManyField(Skill, verbose_name=_("Skills"))
    description = models.TextField(_("Description"), null=True, blank=True, max_length=200)
    users = models.ManyToManyField(User, through='User_Project', verbose_name=_("User_Project"), blank=True,
                                   related_name='users_projects')
    duration = models.DurationField(_("Duration"))
    create_date = models.DateTimeField(_("Create_Date"), auto_now_add=True)
    situation = models.CharField(_("Project_Situation"), max_length=7, choices=SITUATION_CHOICES)
    admin = models.ForeignKey(User, verbose_name=_("Scrum_Master"), blank=True, on_delete=models.PROTECT,
                              related_name='admin_projects')
    creator = models.ForeignKey(User, verbose_name=_("Project_Owner"), blank=True, on_delete=models.PROTECT,
                                related_name='created_projects')

    def __str__(self):
        return self.name

    def date_created_decorated(self):
        return jdatetime.datetime.fromgregorian(datetime=self.create_date).strftime("%a, %d %b %Y %H:%M:%S")

    date_created_decorated.short_description = _("date_created_decorated")

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Project")
        verbose_name = _("Project")


class User_Project(models.Model):
    SITUATION_CHOICES = (
        ('ACCEPTED', _("Accepted")),
        ('REQUESTED', _("Requested")),
        ('DECLINED', _("Declined")),
    )
    project = models.ForeignKey(Project, verbose_name=_("Project"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    situation = models.CharField(max_length=9, verbose_name=_("Situation"), choices=SITUATION_CHOICES)


class Temp(models.Model):
    email = models.EmailField(verbose_name=_("Email"), validators=[validate_email], max_length=255)
    date = models.DateTimeField(verbose_name=_("Date"), auto_now=True)
    code = models.CharField(verbose_name=_("Code"), max_length=20)

    class Meta:
        ordering = ['date']
        verbose_name = _("Temps")
        verbose_name_plural = _("Temps")
