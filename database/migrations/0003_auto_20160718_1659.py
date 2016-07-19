# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20160717_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='account_type',
            field=models.IntegerField(default=1, choices=[(1, b'Customer: (Pay per transaction)'), (2, b'Shop Administrator: (Got a shop?)'), (3, b'Laundry Bear Administrator'), (4, b'Subscriber: (Just pay every month!)')]),
        ),
    ]
