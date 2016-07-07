# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_admin_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laundryshop',
            name='contact_number',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(b'^/\\+?([0-9][\\s-]?){10,13}/', b'Invalid input!')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='contact_number',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(b'^/\\+?([0-9][\\s-]?){10,13}/', b'Invalid input!')]),
        ),
    ]
