import jdatetime
from imagekit.models import ProcessedImageField
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from core import validators
from core.models import AbstractImageModel
from accounts.managers import UserManager
from core.validators import PDF_TYPE_VALIDATOR


class User(AbstractBaseUser, PermissionsMixin, AbstractImageModel):
    IMAGE_PROCESS = {**AbstractImageModel.IMAGE_PROCESS, **{"default": "defaults/default.png"}}

    @classmethod
    def getImageField(cls):
        return "avatar"

    @classmethod
    def getImageName(clsc):
        return "username"

    @classmethod
    def getUploadTo(cls):
        return "user/avatars/"

    GENDER_CHOICES = (
        ('MALE', _("male")),
        ('FEMALE', _("female")),
    )

    username = models.CharField(_("Username"), max_length=30, unique=True,
                                validators=[validators.CHAR_REGEX_VALIDATOR], )
    password = models.CharField(_("Password"), max_length=128)
    email = models.EmailField(_("Email"), max_length=254, unique=True, )
    phone_number = PhoneNumberField(_("Phone_Number"), null=True, blank=True, unique=True, region='IR')
    first_name = models.CharField(_("First_Name"), max_length=30, validators=[validators.PERSIAN_REGEX_VALIDATOR])
    last_name = models.CharField(_("Last_Name"), max_length=30, validators=[validators.PERSIAN_REGEX_VALIDATOR])
    gender = models.CharField(_("Gender"), max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    # avatar = models.ImageField(_("Avatar"), null=True, blank=True, upload_to='avatars/')
    avatar = ProcessedImageField(**IMAGE_PROCESS)
    is_active = models.BooleanField(_("Is_Active"), default=True)
    # is_superuser is already used into AbstractBaseUser and only i override it instead of create otherfield
    is_superuser = models.BooleanField(_("Is_Superuser"), default=False)
    joined_date = models.DateTimeField(_("Joined_Date"), auto_now_add=True)
    description = models.TextField(_("Description"), null=True, blank=True, max_length=200)
    university = models.ForeignKey("University", verbose_name=_("University_Name"), on_delete=models.SET_NULL,
                                   null=True, blank=True)
    city = models.ForeignKey("City", verbose_name=_("City"), on_delete=models.SET_NULL, null=True, blank=True)
    skills = models.ManyToManyField("Skill", verbose_name=_("Skill"), blank=True)
    resume = models.FileField(_("resume"), blank=True, null=True, upload_to='user/resume/',
                              validators=[PDF_TYPE_VALIDATOR])

    class Meta:
        ordering = ['username']
        verbose_name_plural = _("Users")
        verbose_name = _("User")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', ]

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def joined_date_decorated(self):
        return jdatetime.datetime.fromgregorian(datetime=self.joined_date).strftime("%a, %d %b %Y %H:%M:%S")

    joined_date_decorated.short_description = _("Joined_Date_Decorated")

    @property
    def is_staff(self):
        return self.is_superuser

    def get_full_name(self):
        return ('%s %s' % (self.first_name, self.last_name)).strip()
