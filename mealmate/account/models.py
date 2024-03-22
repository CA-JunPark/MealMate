from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from mealmate.settings import MEDIA_ROOT

class AccountManager(BaseUserManager):
    def create_user(self, username, password, email):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=self.username,
            password=self.password,
            email=self.normalize_email(email),  # lowercasing
            photo=self.photo,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    # password field is inherited from AbstractBaseUser
    username = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(verbose_name='email',
                              max_length=255, unique=True,)
    
    photo = models.TextField(default="media/default_profile.png")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'account'
