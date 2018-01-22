from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_unixdatetimefield import UnixDateTimeField


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    driver = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Trip(models.Model):
    user = models.ForeignKey(User, related_name='trips', on_delete=models.CASCADE)
    name = models.TextField(max_length=500, blank=False)
    start = UnixDateTimeField()
    end = UnixDateTimeField()

    def __str__(self):
        return self.name

    def clean(self):
        if not self.user.profile.driver:
            raise ValidationError({'user': 'Only drivers are allowed to register trips.'})
