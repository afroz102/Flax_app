# import datetime
# from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models
from django.contrib.auth.models import User


# from django.contrib.auth.models import AbstractUser


GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)


# class User(AbstractUser):
#     profession_title = models.CharField(max_length=200, blank=True)
#     phone = models.CharField(max_length=200, blank=True)
#     gender = models.CharField(max_length=20, choices=GENDER, blank=True)
#     age = models.PositiveIntegerField(blank=True)
#     location = models.CharField(max_length=250, blank=True)
#     profile_img = models.ImageField(upload_to='profile_img/', blank=True)
#
#     about_me = models.TextField(blank=True)
#
#     is_verified = models.BooleanField(default=False)
#
#     sent_for_verification = models.BooleanField(default=False)
#
#     is_deleted = models.BooleanField(default=False)
#
#     def __str__(self):
#         if self.first_name:
#             return f"{self.first_name} {self.last_name}"
#         return str(self.id)
#
#     @property
#     def full_name(self):
#         return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession_title = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, blank=True)
    age = models.PositiveIntegerField(blank=True)
    location = models.CharField(max_length=250, blank=True)
    profile_img = models.ImageField(upload_to='profile_img/', blank=True)

    about_me = models.TextField(blank=True)

    is_verified = models.BooleanField(default=False)

    sent_for_verification = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.user.first_name:
            return self.user.first_name + '-' + self.user.last_name
        return str(self.id)

    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name


# # For validating min and max Year
# def current_year():
#     return datetime.date.today().year
#
#
# def max_value_current_year(value):
#     return MaxValueValidator(current_year())(value)

# class EmployeesTrainings(models.Model):
#     name = models.ForeignKey(employee, default='',
#                              blank=True, null=True, on_delete=models.CASCADE)
#     training_name = models.TextField(
#         max_length=200, default='', blank=False, null=False)
#     training_year = models.PositiveIntegerField(
#         default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
