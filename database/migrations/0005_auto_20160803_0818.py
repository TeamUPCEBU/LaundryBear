# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_reloadrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='laundryshop',
            name='credits',
            field=models.PositiveIntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='reloadrequest',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
