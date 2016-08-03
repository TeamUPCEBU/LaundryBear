from decimal import *
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.sites.models import Site
from datetime import timedelta, datetime
from django.core.validators import RegexValidator

#from rest_framework.authtoken.models import Token
#Models are also known as tables
#Each field is an attribute of the table
#Models are still classes and can have methods within


#Generate tokens for all existing users
#for user in User.objects.all():
#    Token.objects.get_or_create(user=user)

contactNumberValidator = RegexValidator(r'^\+?([\d][\s-]?){10,13}$', 'Invalid input!')
class UserProfile(models.Model):

    CUSTOMER = 1
    SHOPADMIN = 2
    LAUNDRYBEARADMIN = 3
    SUBSCRIBER = 4

    ACCOUNT_TYPE_CHOICES = (
        (CUSTOMER, 'Customer: (Pay per transaction)'),
        (SHOPADMIN, 'Shop Administrator: (Got a shop?)'),
        (LAUNDRYBEARADMIN, 'Laundry Bear Administrator'),
        (SUBSCRIBER, 'Subscriber: (Just pay every month!)')
    )

    account_type = models.IntegerField(choices=ACCOUNT_TYPE_CHOICES, default=1)
    user = models.OneToOneField(User)
    province = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=True)
    barangay = models.CharField(max_length=50, blank=False)
    street = models.CharField(max_length=50, blank=True)
    building = models.CharField(max_length=50, blank=True)
    contact_number = models.CharField(max_length=30, blank=False,
                        unique=True, validators=[contactNumberValidator])

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

    PENDING = 1
    ACTIVE = 2
    INACTIVE = 3
    REJECTED = 4

    LAUNDRY_SHOP_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (REJECTED, 'Rejected')
    )

    admin = models.OneToOneField(UserProfile, related_name='laundry_shop')
    status = models.IntegerField(choices=LAUNDRY_SHOP_STATUS_CHOICES, default=1)
    name = models.CharField(max_length=50, blank=False)
    website = models.URLField(blank=True)
    opening_time = models.TimeField(blank=False, auto_now=False, auto_now_add=False)
    closing_time = models.TimeField(blank=False, auto_now=False, auto_now_add=False)
    days_open = models.CharField(max_length=100, blank=False)
    credits = models.PositiveIntegerField(default=50)
    creation_date = models.DateTimeField(auto_now_add=True)

    @property
    def email(self):
        return self.admin.user.email

    @property
    def contact_number(self):
        return self.admin.contact_number


    @property
    def hours_open(self):
        return (str(datetime.strptime(str(self.opening_time), "%H:%M:%S").strftime("%I:%M %p")) + " - "  +
               str(datetime.strptime(str(self.closing_time), "%H:%M:%S").strftime("%I:%M %p")))


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
                    order__price__laundry_shop=self, paws__isnull=False)
        average = t.aggregate(models.Avg('paws'))
        return average['paws__avg']

    @property
    def raters(self):
        return len(Transaction.objects.filter(
                    order__price__laundry_shop=self, paws__isnull=False))

    @property
    def comments(self):
        return Transaction.objects.filter(
                    order__price__laundry_shop=self,
                    comment__isnull=False).exclude(comment='').values_list('client__user__first_name',
                                                                           'client__user__last_name',
                                                                           'paws', 'comment')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.opening_time < self.closing_time:
            super(LaundryShop, self).save(*args, **kwargs)
        self.admin.account_type = 2
        self.admin.save()


class Service(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.TextField(blank=False)
    prices = models.ManyToManyField('LaundryShop', through='Price',
        related_name='services')

    def __unicode__(self):
        return self.name


class Price(models.Model):
    laundry_shop = models.ForeignKey('LaundryShop', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    duration = models.IntegerField()


class Order (models.Model):
    price = models.ForeignKey('Price')
    transaction = models.ForeignKey('Transaction')
    pieces = models.IntegerField(default=0)

def default_date():
    return timezone.now()+timedelta(days=3)


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
    fee = models.ForeignKey('Fees', related_name='fees')
    discount = models.DecimalField(decimal_places=2, default=0.0, max_digits=6)

    @property
    def location(self):
    	address = [self.building, self.street, self.barangay,
                   self.city, self.province]
        while '' in address:
        	address.remove('')
        return ', '.join(address)

    def __unicode__(self):
        return "{0}".format(unicode(self.request_date))


    @property
    def num_of_clothes(self):
        return Order.objects.filter(transaction__pk=self.pk).values('pieces').aggregate(sum=Sum('pieces'))['sum']


class Fees(models.Model):
    delivery_fee = models.DecimalField(default=50, decimal_places=2,
        max_digits=4)
    service_charge = models.DecimalField(default=0.1, decimal_places=2,
        max_digits=3)
    site = models.OneToOneField(Site)

    def __unicode__(self):
        return 'Regular rate'


class ReloadRequest(models.Model):
    amount = models.PositiveIntegerField(default=0)
    requestor = models.ForeignKey('UserProfile')

    def __unicode__(self):
        return str(self.requestor) + ": " + str(self.amount) + " credits"
