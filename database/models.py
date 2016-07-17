from decimal import *
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator
from django.core import serializers as serial

from rest_framework.authtoken.models import Token

contactNumberValidator = RegexValidator(r'^\+?([\d][\s-]?){10,13}$', 'Invalid input!')
days_open_validator = RegexValidator(r'([0]|[1]){7,7}$', 'Invalid input!')
class UserProfile(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        (1, 'Customer'),
        (2, 'Shop Administrator'),
        (3, 'Laundry Bear Administrator'),
        (4, 'Subscriber')
    )

    account_type = models.IntegerField(choices=ACCOUNT_TYPE_CHOICES, default=1)
    user = models.OneToOneField(User, related_name='userprofile')
    province = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=True)
    barangay = models.CharField(max_length=50, blank=False)
    street = models.CharField(max_length=50, blank=True)
    building = models.CharField(max_length=50, blank=True)
    contact_number = models.CharField(max_length=30, blank=False,
                                validators=[contactNumberValidator])

    def __unicode__(self): #Default return value of the UserProfile
        return self.user.get_full_name()

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

    admin = models.OneToOneField(UserProfile, related_name='laundry_shop')
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
        t = Transaction.objects.filter(
                    orders__price__laundry_shop=self, paws__isnull=False)
        average = t.aggregate(models.Avg('paws'))
        return average['paws__avg']

    @property
    def raters(self):
        return len(Transaction.objects.filter(
                    orders__price__laundry_shop=self, paws__isnull=False))

    @property
    def comments(self):
        return Transaction.objects.filter(
                    orders__price__laundry_shop=self,
                    comment__isnull=False).exclude(comment='').values_list('comment')


    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.opening_time < self.closing_time:
            super(LaundryShop, self).save(*args, **kwargs)
        self.admin.account_type = 2
        self.admin.save()



def default_date():
    return timezone.now()+timedelta(days=3)


class Service(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.TextField(blank=False)
    prices = models.ManyToManyField('LaundryShop', through='Price',
        related_name='services')

    def __unicode__(self):
        return self.name


class Price(models.Model):
    laundry_shop = models.ForeignKey('LaundryShop', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='price_set')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    duration = models.IntegerField()


class Order (models.Model):
    price = models.ForeignKey('Price')
    transaction = models.ForeignKey('Transaction', related_name='orders')
    pieces = models.IntegerField(default=0)


class Transaction(models.Model):
    class Meta:
        get_latest_by = 'request_date'

    TRANSACTION_STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Ongoing'),
        (3, 'Done'),
        (4, 'Rejected'),
        (5, 'Broadcasted')
    )

    def get_choice_name(self):
        return self.TRANSACTION_STATUS_CHOICES[self.status - 1][1]

    paws = models.IntegerField(blank=True, null=True)
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
    client = models.ForeignKey('UserProfile', related_name='transactions')
    comment = models.TextField(blank=True, null=True)
    fee = models.ForeignKey('Fee', related_name='fee')

    @property
    def location(self):
    	return self.admin.location

    def __unicode__(self):
        return "{0}".format(unicode(self.request_date))


class Fee(models.Model):
    delivery_fee = models.DecimalField(default=50, decimal_places=2,
        max_digits=4)
    service_charge = models.DecimalField(default=0.1, decimal_places=2,
        max_digits=3)
    name = models.CharField(blank=False, max_length=100)

    def __unicode__(self):
        return (self.name)
