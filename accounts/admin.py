from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from jalali_date.admin import ModelAdminJalaliMixin
from .forms import UserForm
from .models import *

admin.site.site_header = _("Admin_page")
admin.site.index_title = _("Manage_Model")


class UserProjectsInline(admin.TabularInline):
    model = UserProject
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if isinstance(obj, User):
            return ('status',)
        else:
            return super(UserProjectsInline, self).get_readonly_fields(request, obj)



class UserAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'is_active')
    readonly_fields = ('joined_date_decorated',)
    list_filter = ('is_active',)
    form = UserForm
    fields = ('username', 'email', 'password1', 'password2', 'joined_date_decorated',
              'first_name', 'last_name', 'avatar', 'gender', 'description',
              'is_superuser', 'is_active', 'city', 'university', 'skills', 'resume','phone_number')
    inlines = [UserProjectsInline]


class CityInline(admin.TabularInline):
    model = City
    extra = 0
    fields = ('code', 'name')


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    fields = ('code', 'name')
    inlines = [CityInline]


class ProjectsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'status', 'end_date_decorated')
    fields = ('name', 'description', 'status', 'last_modified_date', 'start_date', 'end_date')
    inlines = [UserProjectsInline]


admin.site.register(Temp)
admin.site.register(User, UserAdmin)
admin.site.register(University)
admin.site.register(Project, ProjectsAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Skill)
admin.site.unregister(Group)
