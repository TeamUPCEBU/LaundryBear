# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20160801_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='transaction',
            field=models.OneToOneField(null=True, blank=True, to='database.Transaction'),
        ),
        migrations.AlterField(
            model_name='point',
            name='user',
            field=models.OneToOneField(to='database.UserProfile'),
        ),
    ]
