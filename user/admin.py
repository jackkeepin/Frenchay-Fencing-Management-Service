from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User

# Register your models here.

class MyUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_num')
    search_fields = ('email', 'first_name')
    readonly_fields = ('id',)
    ordering = ('email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_num' , 'password1', 'password2'),
        }),
    )



admin.site.register(User, MyUserAdmin)