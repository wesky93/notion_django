# Create your models here.
import logging

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models, models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from passwords.validators import ComplexityValidator, LengthValidator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, nickname, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            **extra_fields,
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, nickname, password, **extra_fields)

    def create_superuser(self, email, nickname, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, nickname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    email = models.EmailField(unique=True, )
    nickname_validator = UnicodeUsernameValidator()
    nickname = models.CharField(
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[nickname_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        verbose_name='nickname'
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', ]

    def password_validated(self, password):
        validates = [
            ComplexityValidator(complexities=settings.PASSWORD_COMPLEXITY),
            LengthValidator(min_length=settings.PASSWORD_MIN_LENGTH, max_length=settings.PASSWORD_MAX_LENGTH)
        ]
        for v in validates:
            v(password)

    def set_password(self, raw_password):
        self.password_validated(raw_password)
        super().set_password(raw_password)
