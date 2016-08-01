# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_auto_20160801_0104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reward',
            name='points',
        ),
        migrations.AddField(
            model_name='point',
            name='cycle',
            field=models.IntegerField(default=0),
        ),
    ]
