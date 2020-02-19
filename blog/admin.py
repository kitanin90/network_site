from django.contrib import admin
from .models import  Account, Community, Contact, ConnectCommunityPeople
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from blog.forms import RegisterForm


class AccountUserAdmin(UserAdmin):
    add_form = RegisterForm
    model = Account

    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth')
    list_filter = ('username', 'is_superuser')

    # Поля пользователя
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'password')}),
    )
    # Поля при добавлении пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'last_name', 'first_name', 'password1', 'password2')}
         ),
    )

    search_fields = ('username', 'email')
    ordering = ('username', 'email')


class CommunityAdmin(admin.ModelAdmin):
    model = Community

    list_display = ('name', 'description', 'creator', 'img_community')
    list_filter = ('name', 'creator')



admin.site.register(Account, AccountUserAdmin)
admin.site.register(Contact)
admin.site.register(Community, CommunityAdmin)
admin.site.register(ConnectCommunityPeople)
