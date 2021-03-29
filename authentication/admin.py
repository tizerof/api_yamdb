from django.contrib import admin

from .models import User, UserConfirmation


class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ('email', 'confirmation_code')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role',
                    'bio', 'first_name', 'last_name', 'is_staff')


admin.site.register(UserConfirmation, UserConfirmationAdmin)
admin.site.register(User, UserAdmin)
