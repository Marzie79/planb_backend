from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserChangeForm, UserCreationForm
from .models import *
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin
from jalali_date import datetime2jalali
import jdatetime

admin.site.site_header = 'صفحه ادمین'
admin.site.index_title = 'مدیریت مدل ها'

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserChangeForm
#     add_form = UserCreationForm
#
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('__str__', 'email', 'is_admin')
#     list_filter = ('is_admin',)
#     fieldsets = (
#         (None, {
#             'fields': ('email', 'password', 'username', 'first_name', 'last_name')}),
#         ('Permission', {'fields': ('is_admin', 'is_active')}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2'),
#         }),
#     )
#     search_fields = ('email', 'username')
#     ordering = ('last_name',)
#     filter_horizontal = ()
#
#
# @admin.register(Temp)
# class TempAdmin(admin.ModelAdmin):
#     fields = ('email', 'code')
#     list_display = ('email', 'code')


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
			 ('اطلاعات شخص', {'fields': (
            'first_name', 'last_name', 'avatar', 'gender', 'description')}),
         ('دسترسی ها', {'fields': ('is_admin', 'is_active')}),
		('آدرس', {'fields': ('city', 'university')}),
		('مهارت ها', {'fields': ('skills',)}))
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
	list_display = ('name', 'creator', 'situation','duration')
	readonly_fields = ('date_created_decorated',)
	fieldsets = ((None, {'fields': ('name','creator', 'description')}),
				('ویژگی ها', {'fields': ('skills', 'situation')}), (None, {'fields': ('date_created_decorated', 'duration')}))


admin.site.register(Temp)
admin.site.register(User, UserAdmin)
admin.site.register(University)
admin.site.register(Project, ProjectsAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Skill)
admin.site.unregister(Group)
