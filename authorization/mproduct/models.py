"""
Database info
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.

class Subscriber(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    company = models.CharField(max_length=30,help_text="Company Name")
    companysize = models.IntegerField(help_text="Company size")
    registered_on = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username}'
    

# @receiver(post_save,sender=User)
# def create_or_update_subscriber_profile(sender,instance,created,**kwargs):
#     if created:
#         Subscriber.objects.create(user=instance)
#     else:
#         if hasattr(instance,'subscriber'):
#             instance.subscriber.save()
#         else:
#             Subscriber.objects.create(user=instance)


class Company(models.Model):
    """
    Model to store info about variouos Companys
    """
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=30,unique=True)

    class Meta:
        unique_together = ('owner','name')

    def __str__(self) -> str:
        return self.name


class BusinessUnit(models.Model):
    """
    Model to store info about BusinessUnits from various Companys
    """
    name = models.CharField(verbose_name="BusinessUnit name",max_length=20,unique=True)
    Company = models.ForeignKey(Company,on_delete=models.CASCADE)
    head = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self) -> str:
        return f'{self.Company}-{self.name}'


class Employee(models.Model):
    """
    Model to store info about employees from different companies
    """
    employee = models.OneToOneField(User,on_delete=models.CASCADE)
    BusinessUnit = models.ForeignKey(BusinessUnit,on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.employee}-{self.BusinessUnit.Company}'


class Requests(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_requests')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='received_requests')
    created = models.DateField()
    status = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.created}-{self.sender}'

class Plans(models.Model):
    """
    Model to store information about the plans that the admin offers.
    """
    slug = models.SlugField(unique=True,blank=True)
    name = models.CharField(max_length=50,blank=False)
    Company = models.ForeignKey(Company,on_delete=models.CASCADE)
    description = models.CharField(max_length=255,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    duration = models.IntegerField(help_text="Duration of the plan")

    def save(self,*args,**kwargs):
        self.slug = slugify(f'{self.Company.owner.username}-{self.Company.name}-{self.name}-{self.price}-{self.duration}')
        super(Plans,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return f'{self.slug}'
