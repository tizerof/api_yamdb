from django.contrib import admin

from .models import UserConfirmation


class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ('email', 'confirmation_code')


admin.site.register(UserConfirmation, UserConfirmationAdmin)
