from Common.models import BaseModel
from django.db import models
from Auth.models import User


class Company(BaseModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)