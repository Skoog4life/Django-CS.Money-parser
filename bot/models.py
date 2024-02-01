from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()

class TelegramUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    chat_id = models.CharField(max_length=20, primary_key=True)
    notify = models.BooleanField(default=True)

    def has_staff_status(self):
        if self.user:
            return self.user.is_staff
        return False

    def __str__(self):
        return self.chat_id
    
    