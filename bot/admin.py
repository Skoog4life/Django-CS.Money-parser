from django.contrib import admin
from bot.models import TelegramUser
# Register your models here.

class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'user']

admin.site.register(TelegramUser, TelegramUserAdmin)