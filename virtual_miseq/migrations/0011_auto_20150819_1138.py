# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0010_idmsuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idmsuser',
            name='AuthenticationString',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'Authentication String', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Billingaddress',
            field=models.CharField(max_length=150, null=True, verbose_name=b'Billing Address', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Billingcity',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Billing City', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Billingstate',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Billing State', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Billingzip',
            field=models.IntegerField(null=True, verbose_name=b'Billin ZIP', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='NTID',
            field=models.CharField(max_length=20, null=True, verbose_name=b'NTID', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Password',
            field=models.CharField(default=b'', max_length=32, verbose_name=b'Password', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Phone',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'Phone', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Shippingaddress',
            field=models.CharField(max_length=150, null=True, verbose_name=b'Shipping Adress', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Shippingbuilding',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Shipping Building', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Shippingcity',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Shipping City', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Shippingroom',
            field=models.CharField(max_length=45, null=True, verbose_name=b'Shipping Room', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Shippingstate',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Shipping State', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Shippingzip',
            field=models.IntegerField(null=True, verbose_name=b'Shipping ZIP', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='Username',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'User Name', blank=True),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='role',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'analyst', b'analyst'), (b'supervisor', b'supervisor')]),
        ),
        migrations.AlterField(
            model_name='idmsuser',
            name='user_group',
            field=models.CharField(default=b'', max_length=30, verbose_name=b'User Group', blank=True),
        ),
    ]
