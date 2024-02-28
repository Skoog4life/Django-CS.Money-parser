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