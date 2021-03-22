from django.contrib import admin

from .models import UserConfirmation, Profile


class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ('email', 'confirmation_code')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role',
                    'bio', 'first_name', 'last_name')


admin.site.register(UserConfirmation, UserConfirmationAdmin)
admin.site.register(Profile, ProfileAdmin)
