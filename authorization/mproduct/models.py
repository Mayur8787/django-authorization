"""
Database info
"""

from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.


class Brand(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=30,unique=True)

    class Meta:
        unique_together = ('owner','name')

    def __str__(self) -> str:
        return self.name

class Plans(models.Model):
    """
    Model to store information about the plans that the admin offers.
    """
    slug = models.SlugField(unique=True,blank=True)
    name = models.CharField(max_length=50,blank=False)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    description = models.CharField(max_length=255,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,unique=True)
    duration = models.IntegerField(help_text="Duration of the plan")

    def save(self,*args,**kwargs):
        self.slug = slugify(f'{self.brand.owner.username}-{self.brand.name}-{self.name}-{self.price}-{self.duration}')
        super(Plans,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return f'{self.slug}'

class Subscribers(models.Model):
    name = models.ForeignKey(User,related_name='subscriber',on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans,related_name='plan',on_delete=models.CASCADE)
    purchased_on = models.DateField()
    subscription_status = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.name}-{self.plan}'
