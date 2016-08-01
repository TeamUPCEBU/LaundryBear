# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_auto_20160801_0110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='point',
            name='cycle',
        ),
        migrations.AlterField(
            model_name='point',
            name='transaction',
            field=models.ForeignKey(blank=True, to='database.Transaction', null=True),
        ),
        migrations.AlterField(
            model_name='point',
            name='user',
            field=models.ForeignKey(to='database.UserProfile'),
        ),
    ]
