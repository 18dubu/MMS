# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0002_auto_20150805_1825'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=500)),
                ('content', models.TextField()),
                ('visible_to', models.CharField(default=b'Collaborators', max_length=20, blank=True, choices=[(b'Everyone', b'Everyone'), (b'Me', b'Me'), (b'Collaborators', b'Collaborators')])),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Created Date', blank=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name=b'Updated date', null=True)),
                ('download_date', models.DateTimeField(null=True, verbose_name=b'Download Date', blank=True)),
                ('created_by', models.ForeignKey(related_name='log_created_by', blank=True, to='virtual_miseq.IDMSUser', null=True)),
                ('download_by', models.ManyToManyField(related_name='log_download_by', to='virtual_miseq.IDMSUser', blank=True)),
                ('related_exp', models.ManyToManyField(related_name='log_related_exp', to='virtual_miseq.Experiment', blank=True)),
                ('related_sam', models.ManyToManyField(related_name='log_related_sam', to='virtual_miseq.Sample', blank=True)),
                ('updated_by', models.ManyToManyField(related_name='log_updated_by', to='virtual_miseq.IDMSUser', blank=True)),
                ('writer', models.ManyToManyField(related_name='writer', to='virtual_miseq.IDMSUser')),
            ],
        ),
    ]
