from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Subscription


class UserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
