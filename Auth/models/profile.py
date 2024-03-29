from Common.models import BaseModel
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(BaseModel):
    TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('super', 'Super'),
        ('company', 'Company'),
    ]

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    handle = models.CharField(max_length=50)
    number_of_followers_onboarded = models.IntegerField(default=0)
    network = models.CharField(max_length=50)
    bank_account = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=50)