from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


def create_member_for_user(user):
    return Member.objects.create(user=user)
