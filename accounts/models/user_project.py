import jdatetime
from datetime import datetime, timedelta
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProject(models.Model):
    STATUS_CHOICES = (
        ('ACCEPTED', _("Accepted")),
        ('PENDING', _("Pending")),
        ('DECLINED', _("Declined")),
        ('DELETED', _("Deleted")),
        ('ADMIN', _("Admin")),
        ('CREATOR', _("Project_Owner")),

    )
    project = models.ForeignKey("Project", verbose_name=_("Project"), on_delete=models.CASCADE)
    user = models.ForeignKey("User", verbose_name=_("User"), on_delete=models.CASCADE)
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
