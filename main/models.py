from django.db import models


class User_Data(models.Model):
    nickname = models.CharField('Nickname', max_length = 20)
    email = models.CharField('email', max_length = 30)
    password = models.CharField('password', max_length = 16)

    def __str__(self):
        return self.nickname
    
#class Watchlist(models.Model):

# Create your models here.

