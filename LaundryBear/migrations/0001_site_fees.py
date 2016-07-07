# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_fees(apps, schema_editor):
    Fees = apps.get_model('database', 'Fees')
    Site = apps.get_model('sites', 'Site')
    fees = Fees(site=Site.objects.get_or_create(domain='laundrybear.pythonanywhere.com')[0])
    fees.save()

class Migration(migrations.Migration):

    dependencies = [
        ('database', '__first__'),
        ('sites', '__first__')
    ]

    operations = [
        migrations.RunPython(create_fees)
    ]
