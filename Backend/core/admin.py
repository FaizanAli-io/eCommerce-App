from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class CustomUserAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        (_('Credentials'), {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2',
                       'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    readonly_fields = ['last_login']


admin.site.register(models.Vendor)
admin.site.register(models.Product)
admin.site.register(models.Consumer, CustomUserAdmin)
