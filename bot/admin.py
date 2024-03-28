from django.contrib import admin
from bot.models import TelegramUser, ItemPrice, FoundItem
# Register your models here.

class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'user']

class FoundItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'name', 'link', 'profit', 'is_sent', 'found_date']
    search_fields = ['name']

class ItemPriceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'update_time']    
    search_fields = ['name']

admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(ItemPrice, ItemPriceAdmin)
admin.site.register(FoundItem, FoundItemAdmin)


# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin
# class UserAdmin(UserAdmin):
#     list_display = ['username', 'email', 'is_staff', 'is_superuser']    
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)