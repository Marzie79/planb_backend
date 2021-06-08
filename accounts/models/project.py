import jdatetime
from datetime import datetime,timedelta

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models import Q

from core.utils import TimeUtils


class Project(models.Model):
    STATUS_CHOICES = (
        ('WAITING', _("Waiting")),
        ('STARTED', _("Started")),
        ('ENDED', _("Ended")),
        ('DELETED', _("Deleted")),
    )
    name = models.CharField(_("Project_Name"), max_length=30, unique=True)
    skills = models.ManyToManyField("Skill", verbose_name=_("Skills"))
    description = models.TextField(_("Description"), null=True, blank=True, max_length=200)
    users = models.ManyToManyField("User", through='UserProject', verbose_name=_("UserProject"), blank=True,
                                   related_name='users_projects')
    end_date = models.DateTimeField(_("End_Date"), default=TimeUtils.one_year_after)
    start_date = models.DateTimeField(_("Start_Date"), default=datetime.now)
    last_modified_date = models.DateTimeField(_("Last_Modify_Date"), default=datetime.now)
    advertisement = models.BooleanField(_("Advertisement"), default=True)
    status = models.CharField(_("Project_Status"), max_length=7, choices=STATUS_CHOICES, default='WAITING')
    slug = models.SlugField(_("Url"), allow_unicode=True, unique=True, blank=True, )
    category = models.ForeignKey("Skill", verbose_name=_('Category'), on_delete=models.PROTECT,
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
        return self.object_update_permission(request.user)

    def object_update_permission(self, user):
        from accounts.models import UserProject
        if self.status != 'ENDED' and self.status != 'DELETED':
            try:
                user_project = UserProject.objects.get(Q(user=user) & Q(project=self))
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
       return self.object_destroy_permission(request.user)

    def object_destroy_permission(self, user):
        from accounts.models import UserProject
        try:
            user_project = UserProject.objects.get(Q(user=user) & Q(project=self))
        except:
            return False
        return user_project.status == 'CREATOR'
