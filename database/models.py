from decimal import *
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator
from django.core import serializers as serial

from rest_framework.authtoken.models import Token
#Models are also known as tables
#Each field is an attribute of the table
#Models are still classes and can have methods within


contactNumberValidator = RegexValidator(r'^\+?([\d][\s-]?){10,13}$', 'Invalid input!')
days_open_validator = RegexValidator(r'([0]|[1]){7,7}$', 'Invalid input!')
class UserProfile(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        (1, 'Customer'),
        (2, 'Shop Administrator'),
        (3, 'Laundry Bear Administrator'),
    )

    account_type = models.IntegerField(choices=ACCOUNT_TYPE_CHOICES, default=1)
    client = models.OneToOneField(User, related_name='userprofile')
    province = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=True)
    barangay = models.CharField(max_length=50, blank=False)
    street = models.CharField(max_length=50, blank=True)
    building = models.CharField(max_length=50, blank=True)
    contact_number = models.CharField(max_length=30, blank=False,
                                validators=[contactNumberValidator])

    def __unicode__(self): #Default return value of the UserProfile
        return self.client.get_full_name()

    @property
    def location(self): #Concatenate address of a user
        address = [self.building, self.street, self.barangay, self.city,
            self.province]
        while '' in address:
            address.remove('') #Remove those that are left blank
        return ', '.join(address)


class LaundryShop(models.Model):
    class Meta:
        get_latest_by = 'creation_date' #Sort

    LAUNDRY_SHOP_STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Active'),
        (3, 'Inactive'),
        (4, 'Rejected')
    )

    admin = models.OneToOneField(UserProfile, related_name='admin')
    status = models.IntegerField(choices=LAUNDRY_SHOP_STATUS_CHOICES, default=1)
    name = models.CharField(max_length=50, blank=False)
    contact_number = models.CharField(max_length=30, blank=False, validators=[contactNumberValidator])
    website = models.URLField(blank=True)
    opening_time = models.TimeField(blank=False, auto_now=False, auto_now_add=False)
    closing_time = models.TimeField(blank=False, auto_now=False, auto_now_add=False)
    days_open = models.CharField(max_length=100, blank=False,
                                 validators=[days_open_validator])
    creation_date = models.DateTimeField(auto_now_add=True)

    @property
    def building(self):
        return self.admin.building

    @property
    def street(self):
        return self.admin.street

    @property
    def barangay(self):
        return self.admin.barangay

    @property
    def city(self):
        return self.admin.city

    @property
    def province(self):
        return self.admin.province

    @property
    def location(self):
        address = [self.admin.building, self.admin.street, self.admin.barangay,
            self.admin.city, self.province]
        while '' in address:
            address.remove('')

        return ', '.join(address)

    @property
    def average_rating(self):
        #TWOPLACES = Decimal(10) ** -2
        #return Decimal(average/total).quantize(TWOPLACES)
        return 0.0

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.opening_time < self.closing_time:
            super(LaundryShop, self).save(*args, **kwargs)
        self.admin.account_type = 2
        self.admin.save()


class Service(models.Model):
    laundry_shop = models.ForeignKey('LaundryShop', related_name='services')
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    duration = models.IntegerField()

    def __unicode__(self):
        return self.name


class Order (models.Model):
    transaction = models.ForeignKey('Transaction')
    service = models.ForeignKey('Service')
    pieces = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.transaction) + " " + str(self.service) + " " + str(self.pieces)

def default_date():
    return timezone.now()+timedelta(days=3)


class Transaction(models.Model):
    class Meta:
        get_latest_by = 'request_date'

    TRANSACTION_STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Ongoing'),
        (3, 'Done'),
        (4, 'Rejected')
    )

    def get_choice_name(self):
        return self.TRANSACTION_STATUS_CHOICES[self.status - 1][1]

    fee = models.ForeignKey('Fees', related_name='fee')
    client = models.ForeignKey('UserProfile', related_name='transactions')
    status = models.IntegerField(choices=TRANSACTION_STATUS_CHOICES, default=1)
    request_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(default=default_date)
    province = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=True)
    barangay = models.CharField(max_length=50, blank=False)
    street = models.CharField(max_length=50, blank=True)
    building = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(blank=False, default=0, max_digits=8,
        decimal_places=2)
    paws = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    @property
    def location(self):
    	return self.admin.location

    def __unicode__(self):
        return "{0}".format(unicode(self.request_date))


class Fees(models.Model):
    delivery_fee = models.DecimalField(default=50, decimal_places=2,
        max_digits=4)
    service_charge = models.DecimalField(default=0.1, decimal_places=2,
        max_digits=3)
    name = models.CharField(blank=False, max_length=100)

    def __unicode__(self):
        return (self.name + "|" + str(self.delivery_fee) +
         " " + str(self.service_charge))
