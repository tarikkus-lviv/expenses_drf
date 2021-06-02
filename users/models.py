import os

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.timezone import now

from expenses.utils.managers import MyUserManager


def get_image_path(filename):
    return os.path.join('user_images', filename)


class PersonManagerQueryset(models.QuerySet):
    def all_users(self):
        return self


class PersonManager(MyUserManager):

    def get_queryset(self):
        return PersonManagerQueryset(self.model, using=self._db)

    use_in_migrations = True


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        (1, "Admin"),
        (2, "User"),
    )
    ROLE_INFO = (
        (1, "Company admin, can login to admin app"),
        (2, "Common user, can login to user app"),
    )

    role = models.IntegerField(verbose_name='Current Role', choices=ROLE_CHOICES, default=2,
                               help_text="Store current user role in system")
    email = models.EmailField('email address', unique=True, null=False)
    full_name = models.CharField('full name', max_length=30, blank=True, default="")
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField('user_photo', upload_to=get_image_path, db_index=True, null=True, blank=True)
    created = models.DateTimeField('date created', default=now)

    is_active = models.BooleanField('active', default=False)
    is_draft = models.BooleanField('draft', default=False)
    is_staff = models.BooleanField('staff', default=False)

    USERNAME_FIELD = 'email'

    objects = PersonManager()

    def __str__(self):
        return "%s" % (str(self.id))

    class Meta(object):
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['full_name']

    def isAdmin(self):
        return self.role == 1

    def isUser(self):
        return self.role == 2

