# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20160803_0818'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='discount',
            field=models.DecimalField(default=0.0, max_digits=6, decimal_places=2),
        ),
    ]
