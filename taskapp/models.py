from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from django.conf import settings
class CustomUser(AbstractUser):

    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    reporting_manager = models.CharField(max_length=20)
    # reporting_manager = models.ForeignKey(
    #     'self',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='reportees',
    #     limit_choices_to={'is_superuser': True}
    # )


class Task(models.Model):
    Categories = [
        ('MTG' , 'Meeting'),
        ('DEV', 'Development'),
        ('BUG', 'Bug fixing'),
        ('FIT', 'Fitness'),
        ('OTH', 'Other')
    ]
    userid = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    task = models.CharField(max_length=50)
    details = models.TextField(blank=True)
    start_date =models.DateField()
    deadline = models.DateField()
    progress = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=10,choices=Categories,default='OTH')


from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
