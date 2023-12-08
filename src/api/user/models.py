from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from api.abstract.models import AbstarctManager, AbstractModel


class UserManager(BaseUserManager, AbstarctManager):
    def create_user(
        self,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        **kwargs,
    ) -> "User":
        if username is None:
            raise TypeError("Require value for `username`.")
        if email is None:
            raise TypeError("Require value for `email`.")
        if password is None:
            raise TypeError("Require value for `password`.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        **kwargs,
    ) -> "User":
        if username is None:
            raise TypeError("Require value for `username`.")
        if email is None:
            raise TypeError("Require value for `email`.")
        if password is None:
            raise TypeError("Require value for `password`.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        db_index=True,
        max_length=255,
        unique=True,
    )
    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        unique_together = ("username", "email")
        db_table = "users"
