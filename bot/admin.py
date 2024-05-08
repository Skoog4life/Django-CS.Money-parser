from django.contrib import admin
from bot.models import TelegramUser, ItemPrice, FoundItem, Config

# Register your models here.


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ["chat_id", "user", "desired_profit", "notify", "language"]


class FoundItemAdmin(admin.ModelAdmin):
    list_display = ["item_id", "name", "link", "profit", "is_sent", "found_date"]
    search_fields = ["name"]


class ItemPriceAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "update_time"]
    search_fields = ["name"]


class ConfigAdmin(admin.ModelAdmin):
    list_display = ["csmoney_allowed_discount", "steam_allowed_profit", "page_count", "time_to_update", "parse_on_start"]


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(ItemPrice, ItemPriceAdmin)
admin.site.register(FoundItem, FoundItemAdmin)
admin.site.register(Config, ConfigAdmin)