from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    Categories = [
        ('MTG' , 'Meeting'),
        ('DEV', 'Development'),
        ('BUG', 'Bug fixing'),
        ('FIT', 'Fitness'),
        ('OTH', 'Other')
    ]
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    task = models.CharField(max_length=50)
    details = models.TextField(blank=True)
    start_date =models.DateField()
    deadline = models.DateField()
    progress = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=10,choices=Categories,default='OTH')



# Create your models here.
