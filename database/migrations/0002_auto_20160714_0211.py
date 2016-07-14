# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='client',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='laundryshop',
            name='admin',
            field=models.OneToOneField(related_name='laundry_shop', to='database.UserProfile'),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction',
            field=models.ForeignKey(related_name='orders', to='database.Transaction'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='account_type',
            field=models.IntegerField(default=1, choices=[(1, b'Customer'), (2, b'Shop Administrator'), (3, b'Laundry Bear Administrator'), (4, b'Subscriber')]),
        ),
    ]
