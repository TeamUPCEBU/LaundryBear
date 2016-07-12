# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import database.models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fees',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delivery_fee', models.DecimalField(default=50, max_digits=4, decimal_places=2)),
                ('service_charge', models.DecimalField(default=0.1, max_digits=3, decimal_places=2)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LaundryShop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Pending'), (2, b'Active'), (3, b'Inactive'), (4, b'Rejected')])),
                ('name', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('barangay', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50, blank=True)),
                ('building', models.CharField(max_length=50, blank=True)),
                ('contact_number', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(b'^\\+?([\\d][\\s-]?){10,13}$', b'Invalid input!')])),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('website', models.URLField(blank=True)),
                ('hours_open', models.CharField(max_length=100)),
                ('days_open', models.CharField(max_length=100)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(related_name='admin', to=settings.AUTH_USER_MODEL)),
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
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('duration', models.IntegerField()),
                ('laundry_shop', models.ForeignKey(related_name='services', to='database.LaundryShop')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Pending'), (2, b'Ongoing'), (3, b'Done'), (4, b'Rejected')])),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateField(default=database.models.default_date)),
                ('province', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('barangay', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50, blank=True)),
                ('building', models.CharField(max_length=50, blank=True)),
                ('price', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('paws', models.IntegerField(null=True, blank=True)),
                ('comment', models.TextField(null=True, blank=True)),
            ],
            options={
                'get_latest_by': 'request_date',
            },
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
                ('contact_number', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(b'^\\+?([\\d][\\s-]?){10,13}$', b'Invalid input!')])),
                ('client', models.OneToOneField(related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='client',
            field=models.ForeignKey(related_name='transactions', to='database.UserProfile'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='fee',
            field=models.ForeignKey(related_name='fee', to='database.Fees'),
        ),
        migrations.AddField(
            model_name='order',
            name='service',
            field=models.ForeignKey(to='database.Service'),
        ),
        migrations.AddField(
            model_name='order',
            name='transaction',
            field=models.ForeignKey(to='database.Transaction'),
        ),
    ]
