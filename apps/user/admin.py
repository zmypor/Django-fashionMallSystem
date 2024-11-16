from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.
from fashionMall.common.options import StackedInline
from .models import fashionMallUser

admin.site.unregister(get_user_model())


class fashionMallUserInline(StackedInline):
    '''Tabular Inline View for fashionMallUser'''

    model = fashionMallUser
    min_num = 1
    max_num = 1
    extra = 1
    readonly_fields = ('balance',)

    
@admin.register(get_user_model())
class fashionMallUserAdmin(UserAdmin):
    '''Admin View for UserAdmin'''
    list_display = ("username", "avatar", 'sex', 'phone', "balance", "is_staff")
    inlines = [
        fashionMallUserInline,
    ]

    @admin.display(description="头像")
    def avatar(self, obj):
        return format_html(
            "<img width='36px' height='36px' src={} />", 
            obj.fashionMalluser.avatar.url if obj.fashionMalluser.avatar else '/static/img/avatar.png'
        )
    
    @admin.display(description="余额")
    def balance(self, obj):
        return obj.fashionMalluser.balance
    
    @admin.display(description="性别")
    def sex(self, obj):
        return obj.fashionMalluser.get_sex_display()
    
    @admin.display(description="手机号")
    def phone(self, obj):
        return obj.fashionMalluser.phone
    