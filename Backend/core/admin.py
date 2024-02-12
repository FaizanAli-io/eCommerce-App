from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class CustomUserAdmin(UserAdmin):
    ordering = ['category']
    list_display = ['email', 'name', 'category']

    fieldsets = (
        (_('Credentials'), {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Category'), {'fields': ('category', )}),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1',
                       'password2', 'category'),
        }),
    )

    readonly_fields = ['last_login']


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Transaction)
admin.site.register(models.ProductStock)
admin.site.register(models.ProductSold)
admin.site.register(models.Product)
admin.site.register(models.Cart)
