# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idmsuser',
            name='EmailAddress',
            field=models.EmailField(default=b'', max_length=255, verbose_name=b'Email Address'),
        ),
    ]
