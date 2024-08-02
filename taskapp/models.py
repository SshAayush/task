from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


    def __str__(self):
        return self.user.username