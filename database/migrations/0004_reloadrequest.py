# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20160718_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReloadRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0.0, max_digits=6, decimal_places=2)),
                ('requestor', models.ForeignKey(to='database.UserProfile')),
            ],
        ),
    ]
