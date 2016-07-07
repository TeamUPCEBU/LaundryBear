# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_auto_20151130_2056'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'get_latest_by': 'request_date'},
        ),
    ]
