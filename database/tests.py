from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from database.models import LaundryShop, Transaction, default_date, UserProfile, Price, Service, Order

# Create your tests here.
class ModelTestCase(TestCase):
    def test_simple_location_property(self):
        shop = LaundryShop.objects.create(name='ls1', province='province1',
            barangay='barangay1', contact_number='12345',
            hours_open='24 hours', days_open='mon - sat')
        expected = 'barangay1, province1'
        self.assertEquals(shop.location, expected)

    def test_complete_location_property(self):
        shop = LaundryShop.objects.create(name='ls1', province='province1',
                city='city1', barangay='barangay1', street='street1',
                building='building1', contact_number='12345612',
                hours_open='12hours', days_open='never')
        expected = 'building1, street1, barangay1, city1, province1'
        self.assertEquals(shop.location, expected)

    def test_average_rating(self):
        shop = LaundryShop.objects.create(name='ls1', province='province1',
            barangay='barangay1', contact_number='12345',
            hours_open='24 hours', days_open='mon - sat')
        client = User.objects.create_user(username='mychelsea', password='mychelsea')
        user_profile = UserProfile.objects.create(client=client,province='province1',
         city='city1', barangay='barangay1', street='street1',
            building='building1', contact_number='123123')
        service = Service.objects.create(name='lol', description='verylol')
        price = Price.objects.create(laundry_shop=shop, service=service, price=45, duration=3)
        transaction1 = Transaction.objects.create(client=user_profile, paws=4, status=3,
            request_date=timezone.now(), 
            delivery_date=timezone.now())
        transaction2 = Transaction.objects.create(client=user_profile, paws=5, status=3,
            request_date=timezone.now(), 
            delivery_date=timezone.now())
        Order.objects.create(price=price, transaction=transaction1, pieces=10)
        Order.objects.create(price=price, transaction=transaction2, pieces=10)
        expected = (4 + 5) / 2.0
        self.assertEquals(shop.average_rating, expected)

    def test_average_rating_no_rating(self):
        shop = LaundryShop.objects.create(name='ls1', province='province1',
            barangay='barangay1', contact_number='12345',
            hours_open='24 hours', days_open='mon - sat')

        client = User.objects.create_user(username='mychelsea', password='mychelsea')
        user_profile = UserProfile.objects.create(client=client,province='province1',
         city='city1', barangay='barangay1', street='street1',
            building='building1', contact_number='123123')
        service = Service.objects.create(name='lol', description='verylol')
        price = Price.objects.create(laundry_shop=shop, service=service, price=45, duration=3)
        transaction1 = Transaction.objects.create(client=user_profile, status=3,
            request_date=timezone.now(), 
            delivery_date=timezone.now())
        transaction2 = Transaction.objects.create(client=user_profile, status=3,
            request_date=timezone.now(), 
            delivery_date=timezone.now())
        Order.objects.create(price=price, transaction=transaction1, pieces=10)
        Order.objects.create(price=price, transaction=transaction2, pieces=10)
        expected = 0
        self.assertEquals(shop.average_rating, expected)

    def test_default_date(self):
        date_today = timezone.now().date()
        actual = default_date().date()
        expected = date_today + timedelta(days=3)
        self.assertEquals(actual, expected)
