from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('developer', 'Developer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class App(models.Model):
    CATEGORY_CHOICES = (
        ('Game', 'Game'),
        ('Education', 'Education'),
        ('Finance', 'Finance'),
    )

    developer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    version = models.CharField(max_length=20)
    image = models.ImageField(upload_to='apps/images/', blank=True, null=True)
    apk_file = models.FileField(upload_to='apps/')
    downloads = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        default='Approved'
    )

    def __str__(self):
        return self.name
    
    
class Review(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()


