from django.conf import settings
from Auth.mixin import MyUserManager
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
import uuid
from datetime import datetime




class User(AbstractBaseUser, PermissionsMixin):
    """
    User data model
    Structure of a user profile
    """

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    GENDER = [("Male", "Male"), ("Female", "Female")]
    TIER = [
        (0, "TIER 0"),
        (1, "TIER 1"),
        (2, "TIER 2"),
        (3, "TIER 3"),
    ]


    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    phone = models.CharField(
        unique=True, help_text="Phone number", max_length=25, null=True
    )
    password = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(choices=GENDER, max_length=255, null=True)
    has_set_password = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    # admin required fields
    is_flagged = models.BooleanField(default=False)
    is_frozen = models.BooleanField(default=False)

    login_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tier = models.IntegerField(choices=TIER, null=False, default=2)
    user_context = models.JSONField(default=dict, null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "users"
        managed = True
        verbose_name = "User"
        verbose_name_plural = "User"

    def __str__(self):
        name = str(self.first_name) + " " + str(self.last_name)
        return self.email + " " + name

    def get_name(self):
        full_name = " ".join(
            filter(None, [self.first_name, self.middle_name, self.last_name]))
        return full_name