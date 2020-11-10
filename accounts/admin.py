from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import UserForm
from .models import *
from jalali_date.admin import ModelAdminJalaliMixin
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _("Admin_page")
admin.site.index_title = _("Manage_Model")


class UserProjectsInline(admin.TabularInline):
    model = UserProject
    extra = 0
    fields = ('project',)


class UserAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'is_active')
    readonly_fields = ('joined_date_decorated',)
    list_filter = ('is_active',)
    form = UserForm
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2', 'joined_date_decorated')}),
        (_("User_Information"), {'fields': (
            'first_name', 'last_name', 'avatar', 'gender', 'description')}),
        (_("Accesses"), {'fields': ('is_superuser', 'is_active')}),
        (_("Address"), {'fields': ('city', 'university')}),
        (_("Skills"), {'fields': ('skills',)}))
    inlines = [UserProjectsInline]


class CityInline(admin.TabularInline):
    model = City
    extra = 0
    fields = ('code', 'name')


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    fieldsets = ((None, {'fields': ('code', 'name')}),)
    inlines = [CityInline]


class ProjectsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'creator', 'situation', 'end_date')
    fieldsets = ((None, {'fields': ('name', 'creator', 'description')}),
                 (_("Priority"), {'fields': ('skills', 'situation')}),
                 (None, {'fields': ('last_modified_date', 'start_date', 'end_date')}))


admin.site.register(Temp)
admin.site.register(User, UserAdmin)
admin.site.register(University)
admin.site.register(Project, ProjectsAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Skill)
admin.site.unregister(Group)
