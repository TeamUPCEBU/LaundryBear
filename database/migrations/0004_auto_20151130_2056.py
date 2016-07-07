# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20151126_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laundryshop',
            name='contact_number',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(b'^\\+?([\\d][\\s-]?){10,13}$', b'Invalid input!')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='contact_number',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(b'^\\+?([\\d][\\s-]?){10,13}$', b'Invalid input!')]),
        ),
    ]
