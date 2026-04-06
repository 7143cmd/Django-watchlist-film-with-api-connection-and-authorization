from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    


class Watchlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='watchlist'
    )
    movie = models.CharField(max_length=9)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.user} - {self.movie}")


# Create your models here.

