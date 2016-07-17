# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laundryshop',
            name='contact_number',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='contact_number',
            field=models.CharField(unique=True, max_length=30, validators=[django.core.validators.RegexValidator(b'^\\+?([\\d][\\s-]?){10,13}$', b'Invalid input!')]),
        ),
    ]
