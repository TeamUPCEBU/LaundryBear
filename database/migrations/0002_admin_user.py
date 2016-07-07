# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.hashers import make_password


def create_admin(app, schema_editor):
    User = app.get_model('auth', 'User')
    admin_password = make_password('laundry')
    admin = User(username='admin', password=admin_password, is_staff=True,
        is_superuser=True, email='admin@laundrybear.com',
        first_name='Laundry Bear', last_name='Administrator')
    admin.save()

    UserProfile = app.get_model('database', 'UserProfile')
    profile = UserProfile(client=admin, barangay='Lahug', province='Cebu',
        city='Cebu City', street='Gorordo Avenue',
        contact_number='09123456789')
    profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin)
    ]
