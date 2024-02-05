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

    def has_staff_status(self):
        if self.user:
            return self.user.is_staff
        return False
    
    def get_desired_profit(self):
        return (self.desired_profit * 100) - 100
    
    def set_desired_profit(self, choosed_profit):
        self.desired_profit = (choosed_profit + 100) / 100
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
