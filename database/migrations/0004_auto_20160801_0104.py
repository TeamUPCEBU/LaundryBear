# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20160718_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acquired', models.DateTimeField(auto_now_add=True)),
                ('used', models.BooleanField(default=False)),
                ('used_on', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.IntegerField(default=0)),
                ('transaction', models.ForeignKey(blank=True, to='database.Transaction', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reward_type', models.IntegerField(default=1, choices=[(1, b'Papa Bear'), (2, b'Mama Bear'), (4, b'Laundry Bear Advocate')])),
                ('service_charge_discount', models.DecimalField(default=0.03, max_digits=3, decimal_places=2)),
                ('delivery_fee_discount', models.DecimalField(default=5, max_digits=4, decimal_places=2)),
                ('points', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='account_type',
            field=models.IntegerField(default=1, choices=[(1, b'Customer: (Pay per transaction)'), (2, b'Shop Administrator: (Got a shop?)'), (3, b'Laundry Bear Administrator')]),
        ),
        migrations.AddField(
            model_name='point',
            name='user',
            field=models.ForeignKey(to='database.UserProfile'),
        ),
        migrations.AddField(
            model_name='award',
            name='awardee',
            field=models.ForeignKey(to='database.UserProfile'),
        ),
        migrations.AddField(
            model_name='award',
            name='reward',
            field=models.ForeignKey(to='database.Reward'),
        ),
    ]
