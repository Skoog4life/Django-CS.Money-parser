from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

# Create your models here.
User = get_user_model()


class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=20, primary_key=True, verbose_name="ID чату")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Користувач")
    desired_profit = models.FloatField(default=1.35, verbose_name="Бажаний прибуток")
    notify = models.BooleanField(default=True, verbose_name="Сповіщати")
    language = models.CharField(max_length=2, default="ua", verbose_name="Мова")

    def has_superuser_status(self):
        if self.user:
            return self.user.is_superuser
        return False

    def has_staff_status(self):
        if self.user:
            return self.user.is_staff
        return False

    def set_user(self, user):
        self.user = user
        self.save()

    def staff_status(self, status):
        self.user.is_staff = status
        # self.user.is_superuser = status
        self.user.save()

    def get_desired_profit(self):
        return round((self.desired_profit * 100) - 100)

    def set_desired_profit(self, choosed_profit):
        self.desired_profit = (choosed_profit + 100) / 100
        self.save()

    def notify_on(self):
        self.notify = True
        self.save()

    def notify_off(self):
        self.notify = False
        self.save()

    def get_language(self):
        return self.language

    def set_language(self, language):
        self.language = language
        self.save()

    def __str__(self):
        return self.chat_id

    class Meta:
        verbose_name = "Телеграм користувач"
        verbose_name_plural = "Телеграм користувачі"

class ItemPrice(models.Model):
    name = models.CharField(primary_key=True, max_length=255, verbose_name="Назва")
    price = models.FloatField(verbose_name="Ціна")
    update_time = models.DateTimeField(auto_now=True, verbose_name="Час оновлення")

    def update_price(self, new_price):
        self.price = new_price
        self.save()

    def need_to_update(self, hours):
        current_time = timezone.now()
        time_difference = current_time - self.update_time
        total_seconds = time_difference.total_seconds()
        return total_seconds >= hours * 60 * 60
    
    class Meta:
        verbose_name = "Ціна предмета"
        verbose_name_plural = "Ціни предметів"


class FoundItem(models.Model):
    item_id = models.CharField(max_length=20, primary_key=True, verbose_name="ID предмета")
    name = models.CharField(max_length=255, verbose_name="Назва")
    link = models.URLField(verbose_name="Посилання")
    csmoney_price = models.FloatField(verbose_name="Ціна на CS.Money")
    steam_price = models.FloatField(verbose_name="Ціна в Steam")
    profit = models.FloatField(verbose_name="Прибуток")
    found_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата знаходження")
    is_sent = models.BooleanField(default=False, verbose_name="Відправлено")

    class Meta:
        verbose_name = "Знайдений товар"
        verbose_name_plural = "Знайдені товари"


class Config(models.Model):
    csmoney_allowed_discount = models.FloatField(default=0.35, verbose_name="Дозволена знижка на CS.Money")
    steam_allowed_profit = models.FloatField(default=1.35, verbose_name="Дозволений прибуток в Steam")
    page_count = models.IntegerField(default=180, verbose_name="Кількість сторінок для парсингу")
    time_to_update = models.IntegerField(default=24, verbose_name="Час оновлення цін")
    parse_on_start = models.BooleanField(default=False, verbose_name="Парсити при запуску")

    def get_csmoney_allowed_discount(self):
        return self.csmoney_allowed_discount * 100

    def set_desired_csmoney_allowed_discount(self, choosed_discount):
        self.csmoney_allowed_discount = round((choosed_discount / 100), 2)
        self.save()

    def set_steam_allowed_profit(self, choosed_profit):
        self.steam_allowed_profit = (choosed_profit + 100) / 100
        self.save()

    def get_steam_allowed_profit(self):
        return (self.steam_allowed_profit * 100) - 100

    def set_page_count(self, page_count):
        self.page_count = page_count * 60
        self.save()

    def get_page_count(self):
        return self.page_count / 60

    def set_time_to_update(self, time_to_update):
        self.time_to_update = time_to_update
        self.save()

    def get_time_to_update(self):
        return self.time_to_update

    def set_parse_on_start(self, parse_on_start):
        self.parse_on_start = parse_on_start
        self.save()

    def get_parse_on_start(self):
        return self.parse_on_start
    
    class Meta:
        verbose_name = "Конфігурація"
        verbose_name_plural = "Конфігурація"
