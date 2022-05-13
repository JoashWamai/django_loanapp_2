from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    CATEGORY = [
        ("Field Officer", "Field Officer"),
        ("Supervisor", "Supervisor"),
        ("Administrator", "Administrator")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="user")
    Category = models.CharField(max_length=100, choices=CATEGORY, verbose_name="Category")
    Photo = models.ImageField(default='avatar.jpg', upload_to="ProfilePictures/", null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.Category}'

