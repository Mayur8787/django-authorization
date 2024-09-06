"""
Database info
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Plans(models.Model):
    """
    Model to store information about the plans that the admin offers.
    """
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=False)
    brand = models.CharField(max_length=30,blank=True)
    description = models.CharField(max_length=255,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    duration = models.DurationField(help_text="Duration of the plan")

    def __str__(self) -> str:
        return f'{self.slug}'

class Subscribers(models.Model):
    name = models.ForeignKey(User,related_name='subscriber',on_delete=models.CASCADE)
    admin = models.ForeignKey(User,related_name='admin',on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans,related_name='plan',on_delete=models.CASCADE)
    purchased = models.DateField(name='Purchased on')
    status = models.BooleanField(name='Subscription status')

    def __str__(self) -> str:
        return f'{self.name}-{self.plan}'
