# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20160714_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'Pending'), (2, b'Ongoing'), (3, b'Done'), (4, b'Rejected'), (5, b'Broadcasted')]),
        ),
    ]
