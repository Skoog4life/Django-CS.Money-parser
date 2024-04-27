from email.policy import default
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

# Create your models here.
User = get_user_model()


class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    desired_profit = models.FloatField(default=1.35)
    notify = models.BooleanField(default=True)
    language = models.CharField(max_length=2, default="ua")

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


class ItemPrice(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    price = models.FloatField()
    update_time = models.DateTimeField(auto_now=True)

    def update_price(self, new_price):
        self.price = new_price
        self.save()

    def need_to_update(self, hours):
        current_time = timezone.now()
        time_difference = current_time - self.update_time
        return time_difference.seconds >= hours * 60 * 60


class FoundItem(models.Model):
    item_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    link = models.URLField()
    csmoney_price = models.FloatField()
    steam_price = models.FloatField()
    profit = models.FloatField()
    found_date = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)


class Config(models.Model):
    csmoney_allowed_discount = models.FloatField(default=0.35)
    steam_allowed_profit = models.FloatField(default=1.35)
    page_count = models.IntegerField(default=180)
    time_to_update = models.IntegerField(default=24)
    parse_on_start = models.BooleanField(default=False)

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
