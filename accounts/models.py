import jdatetime
from datetime import datetime,timedelta
from imagekit.models import ProcessedImageField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import validate_email, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from core import validators
from core.models import AbstractImageModel
from .managers import UserManager
from core.validators import PDF_TYPE_VALIDATOR, SVG_TYPE_VALIDATOR
from django.db.models import Q


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


class Province(models.Model):
    name = models.CharField(_("Province_name"), max_length=20, unique=True)
    code = models.CharField(_("Province_code"), max_length=10, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Provinces")
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
        ordering = ['name']
        verbose_name_plural = _("Cities")
        verbose_name = _("City")
        unique_together = ('name', 'province',)


class University(models.Model):
    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.PROTECT)
    name = models.CharField(_("University_name"), max_length=20)
    code = models.CharField(_("University_code"), max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Universities")
        verbose_name = _("University")
        unique_together = ('name', 'city',)


class Skill(models.Model):
    name = models.CharField(_("Skill_name"), max_length=30, unique=True)
    code = models.CharField(_("Skill_code"), max_length=10, unique=True)
    skill = models.ForeignKey('self', verbose_name=_("Skill's_Father"), on_delete=models.PROTECT,
                              related_name='child_skill',
                              null=True, blank=True)
    image = models.FileField(_("image"), blank=True, null=True, upload_to='skill/image/',
                             validators=[SVG_TYPE_VALIDATOR])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Skills")
        verbose_name = _("Skill")

def one_year_after():
    return datetime.now() + timedelta(days=365)


class Project(models.Model):
    STATUS_CHOICES = (
        ('WAITING', _("Waiting")),
        ('STARTED', _("Started")),
        ('ENDED', _("Ended")),
        ('DELETED', _("Deleted")),
    )
    name = models.CharField(_("Project_Name"), max_length=30, unique=True)
    skills = models.ManyToManyField(Skill, verbose_name=_("Skills"))
    description = models.TextField(_("Description"), null=True, blank=True, max_length=200)
    users = models.ManyToManyField(User, through='UserProject', verbose_name=_("UserProject"), blank=True,
                                   related_name='users_projects')
    end_date = models.DateTimeField(_("End_Date"), default=one_year_after)
    start_date = models.DateTimeField(_("Start_Date"), default=datetime.now)
    last_modified_date = models.DateTimeField(_("Last_Modify_Date"), default=datetime.now)
    advertisement = models.BooleanField(_("Advertisement"), default=True)
    status = models.CharField(_("Project_Status"), max_length=7, choices=STATUS_CHOICES, default='WAITING')
    slug = models.SlugField(_("Url"), allow_unicode=True, unique=True, blank=True, )
    category = models.ForeignKey(Skill, verbose_name=_('Category'), on_delete=models.PROTECT,
                                 related_name='Category', blank=True, null=True)
    amount = models.FloatField(_("amount"), default=float(0), validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['-last_modified_date']
        verbose_name_plural = _("Projects")
        verbose_name = _("Project")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # if not self.slug or self.slug == '':
        self.slug = slugify(self.name, allow_unicode=True)
        if self.status == 'STARTED':
            self.start_date = datetime.now()
        if self.status == 'ENDED':
            self.end_date = datetime.now()
        if self.status == 'ENDED' or self.status == 'DELETED' :
            self.userproject_set.filter(status='PENDING').delete()
        super(Project, self).save()

    def last_modified_date_decorated(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.last_modified_date).strftime("%a, %d %b %Y %H:%M:%S")

    last_modified_date_decorated.short_description = _("Last_Date_Modified_Decorated")

    def start_date_decorated(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.start_date).strftime("%a, %d %b %Y %H:%M:%S")

    start_date_decorated.short_description = _("Start_Date_Decorated")

    def end_date_decorated(self):
        return jdatetime.datetime.fromgregorian(datetime=self.end_date).strftime("%a, %d %b %Y %H:%M:%S")

    end_date_decorated.short_description = _("End_Date_Decorated")

    @property
    def creator(self):
        try:
            return self.userproject_set.get(status='CREATOR').user
        except:
            return None

    creator.fget.short_description = _('Project_Owner')

    @staticmethod
    def has_update_permission(request):
        return True

    def has_object_update_permission(self, request):
        if self.status != 'ENDED' and self.status != 'DELETED':
            try:
                user_project = UserProject.objects.get(Q(user=request.user) & Q(project=self))
            except:
                return False
            is_admin = user_project.status == 'ADMIN'
            is_creator = user_project.status == 'CREATOR'
            return is_admin or is_creator
        return False

    @staticmethod
    def has_create_permission(request):
        if request.user.is_authenticated:
            return True
        return False

    @staticmethod
    def has_destroy_permission(request):
        return True

    def has_object_destroy_permission(self, request):
        try:
            user_project = UserProject.objects.get(Q(user=request.user) & Q(project=self))
        except:
            return False
        return user_project.status == 'CREATOR'


class UserProject(models.Model):
    STATUS_CHOICES = (
        ('ACCEPTED', _("Accepted")),
        ('PENDING', _("Pending")),
        ('DECLINED', _("Declined")),
        ('DELETED', _("Deleted")),
        ('ADMIN', _("Admin")),
        ('CREATOR', _("Project_Owner")),

    )
    project = models.ForeignKey(Project, verbose_name=_("Project"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    status = models.CharField(_("Status"), max_length=9, choices=STATUS_CHOICES, default='PENDING')

    # class Meta:
    #     unique_together = ('project', 'user',)

    def get_role_display(self):
        if self.status == 'ACCEPTED':
            return _("Team_Member")
        return self.get_status_display()

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        query_params = request.query_params
        if ('status' in query_params) and query_params['status'] == 'PENDING':
            if self.user == request.user:
                is_admin = self.status == 'ADMIN'
                is_creator = self.status == 'CREATOR'
                return is_admin or is_creator
            return False
        return True

    @staticmethod
    def has_update_permission(request):
        return True

    def has_object_update_permission(self, request):
        status = self.project.status
        closed_project = status == 'ENDED' or status == 'DELETED'
        validated_username = request.user.username == request.data['user']
        if closed_project:
            return False
        elif request.data['status'] == 'DELETED' and validated_username:
            return True
        elif self.user == request.user:
            is_admin = self.status == 'ADMIN'
            is_creator = self.status == 'CREATOR'
            return is_admin or is_creator
        return False

    @staticmethod
    def has_create_permission(request):
        return True

    def has_object_create_permission(self, request):
        status = self.project.status
        closed_project = status == 'ENDED' or status == 'DELETED'
        validated_username = request.user.username == request.data['user']
        if closed_project:
            return False
        elif request.data['status'] == 'PENDING' and validated_username:
            return True
        elif self.user == request.user:
            is_admin = self.status == 'ADMIN'
            is_creator = self.status == 'CREATOR'
            return is_admin or is_creator
        return False

    class Meta:
        unique_together = ('project', 'user',)


class Temp(models.Model):
    email = models.EmailField(_("Email"), validators=[validate_email], max_length=255)
    date = models.DateTimeField(_("Date"), auto_now=True)
    code = models.CharField(_("Code"), max_length=20)

    class Meta:
        ordering = ['date']
        verbose_name = _("Temp")
        verbose_name_plural = _("Temps")


class Message(models.Model):
    text = models.TextField(_("Text"))
    created_date = models.DateTimeField(_("Created Date"), auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null = True , blank=True)


    class Meta:
        ordering = ['-id']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return self.text

    def created_date_decorated(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_date).strftime("%a, %d %b %Y %H:%M:%S")

    created_date_decorated.short_description = _("Created_Date_Decorated")


class Reciever(models.Model):
    message = models.ForeignKey(Message, verbose_name=_("Message"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    is_visited = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Reciever")
        verbose_name_plural = _("Recievers")
        unique_together = ['message', 'user']

    def __str__(self):
        return "%s - %s"%(self.user, self.message)