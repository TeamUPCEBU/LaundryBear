from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from database.models import UserProfile


# Create your tests here.
class LoginTestCase(TestCase):
    def setUp(self):
        u = User.objects.create_user(username='test', password='runner')
        UserProfile.objects.create(client=u, contact_number='12345',
                                   province='cebu', city='cebu', barangay='lahug')

    def test_login_required_redirect(self):
        response = self.client.get(reverse('client:menu'), follow=True)
        expected = 'client/usersignin.html'
        self.assertTemplateUsed(response, expected)

    def test_redirect_to_menu_after_login_with_next(self):
        response = self.client.get(reverse('client:view-shops'), follow=True)
        request = response.request
        response = self.client.post('{0}?{1}'.format(request['PATH_INFO'],
                                                     request['QUERY_STRING']),
                                    {'username': 'test', 'password': 'runner'}, secure=True,
                                    follow=True)
        expected = 'client/viewshops.html'
        self.assertTemplateUsed(response, expected)

    def test_invalid_login(self):
        response = self.client.get(reverse('client:menu'), follow=True)
        request = response.request
        response = self.client.post('{0}?{1}'.format(request['PATH_INFO'],
                                                     request['QUERY_STRING']),
                                    {'username': 'tester', 'password': 'runner'}, secure=True,
                                    follow=True)
        expected = 'client/usersignin.html'
        self.assertTemplateUsed(response, expected)

    def test_redirect_to_menu_after_login_without_next(self):
        response = self.client.post(reverse('client:login'),
            {'username': 'test', 'password': 'runner'}, secure=True,
            follow=True)
        expected = 'client/dash.html'
        self.assertTemplateUsed(response, expected)

    def test_redirect_to_menu_already_logged_in(self):
        """
        Tests that a redirect will occur if going to the login page manually
        """
        # login
        self.client.post(reverse('client:login'),
                         {'username': 'test', 'password': 'runner'}, secure=True,
                         follow=True)
        response = self.client.get(reverse('client:login'))
        self.assertRedirects(response, reverse('client:menu'))
