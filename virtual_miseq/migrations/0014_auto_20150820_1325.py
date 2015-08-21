# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0013_auto_20150820_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinishedMiseq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('virtual_id', models.CharField(max_length=200, blank=True)),
                ('miSeqId', models.CharField(max_length=200, blank=True)),
                ('analysisId', models.CharField(max_length=200, null=True, blank=True)),
                ('InvestigatorName', models.CharField(max_length=200, null=True, blank=True)),
                ('Date', models.CharField(max_length=200, null=True, blank=True)),
                ('ProjectName', models.CharField(max_length=200, null=True, blank=True)),
                ('ExperimentName', models.CharField(max_length=200, null=True, blank=True)),
                ('refLib', models.CharField(max_length=200, null=True, blank=True)),
                ('Sample_ID', models.CharField(max_length=200, null=True, blank=True)),
                ('Sample_Name', models.CharField(max_length=200, null=True, blank=True)),
                ('group', models.CharField(max_length=200, null=True, blank=True)),
                ('I7_Index_ID', models.CharField(max_length=200, null=True, blank=True)),
                ('index', models.CharField(max_length=200, null=True, blank=True)),
                ('IEMFileVersion', models.IntegerField(null=True, blank=True)),
                ('Workflow', models.CharField(max_length=200, null=True, blank=True)),
                ('Application', models.CharField(max_length=200, null=True, blank=True)),
                ('Assay', models.CharField(max_length=200, null=True, blank=True)),
                ('Description', models.CharField(max_length=200, null=True, blank=True)),
                ('Chemistry', models.CharField(max_length=200, null=True, blank=True)),
                ('CustomRead1PrimerMix', models.CharField(max_length=200, null=True, blank=True)),
                ('Adapter', models.CharField(max_length=200, null=True, blank=True)),
                ('ReverseComplement', models.IntegerField(null=True, blank=True)),
                ('AdapterRead2', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Finished_Miseq',
        ),
    ]
