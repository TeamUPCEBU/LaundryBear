# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import database.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fees',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delivery_fee', models.DecimalField(default=50, max_digits=4, decimal_places=2)),
                ('service_charge', models.DecimalField(default=0.1, max_digits=3, decimal_places=2)),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
        ),
        migrations.CreateModel(
            name='LaundryShop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('barangay', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50, blank=True)),
                ('building', models.CharField(max_length=50, blank=True)),
                ('contact_number', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('website', models.URLField(blank=True)),
                ('hours_open', models.CharField(max_length=100)),
                ('days_open', models.CharField(max_length=100)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'get_latest_by': 'creation_date',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pieces', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('duration', models.IntegerField()),
                ('laundry_shop', models.ForeignKey(to='database.LaundryShop')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField()),
                ('prices', models.ManyToManyField(related_name='services', through='database.Price', to='database.LaundryShop')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paws', models.IntegerField(null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Pending'), (2, b'Ongoing'), (3, b'Done'), (4, b'Rejected')])),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateField(default=database.models.default_date)),
                ('province', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('barangay', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50, blank=True)),
                ('building', models.CharField(max_length=50, blank=True)),
                ('price', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('province', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('barangay', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50, blank=True)),
                ('building', models.CharField(max_length=50, blank=True)),
                ('contact_number', models.CharField(max_length=30)),
                ('client', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='client',
            field=models.ForeignKey(to='database.UserProfile'),
        ),
        migrations.AddField(
            model_name='price',
            name='service',
            field=models.ForeignKey(to='database.Service'),
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.ForeignKey(to='database.Price'),
        ),
        migrations.AddField(
            model_name='order',
            name='transaction',
            field=models.ForeignKey(to='database.Transaction'),
        ),
    ]
