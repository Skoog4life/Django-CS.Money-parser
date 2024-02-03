from django.contrib import admin
from bot.models import TelegramUser, ItemPrice, FoundItem
# Register your models here.

class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'user']

class FoundItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'name', 'link', 'profit', 'is_sent']

admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(ItemPrice)
admin.site.register(FoundItem, FoundItemAdmin)