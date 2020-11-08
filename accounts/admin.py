from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
from jalali_date.admin import ModelAdminJalaliMixin
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _("Admin_page")
admin.site.index_title = _("Manage_Model")


class UserProjectsInline(admin.TabularInline):
    model = User_Project
    extra = 0
    fields = ('project',)


class UserAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'is_active')
    readonly_fields = ('date_joined_decorated',)
    list_filter = ('is_active',)
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password', 'date_joined_decorated')}),
        (_("User_Information"), {'fields': (
            'first_name', 'last_name', 'avatar', 'gender', 'description')}),
        (_("Accesses"), {'fields': ('is_admin', 'is_active')}),
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


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'situation', 'duration')
    readonly_fields = ('date_created_decorated',)
    fieldsets = ((None, {'fields': ('name', 'creator', 'description')}),
                 (_("Priority"), {'fields': ('skills', 'situation')}),
                 (None, {'fields': ('date_created_decorated', 'duration')}))


admin.site.register(Temp)
admin.site.register(User, UserAdmin)
admin.site.register(University)
admin.site.register(Project, ProjectsAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Skill)
admin.site.unregister(Group)
