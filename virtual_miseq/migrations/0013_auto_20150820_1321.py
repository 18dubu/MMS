# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0012_experiment_analyst'),
    ]

    operations = [
        migrations.RenameField(
            model_name='finished_miseq',
            old_name='miseq_id',
            new_name='miSeqId',
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='Adapter',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='AdapterRead2',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='Application',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='Assay',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='Chemistry',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='CustomRead1PrimerMix',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='Date',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='Description',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='ExperimentName',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='I7_Index_ID',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='IEMFileVersion',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='InvestigatorName',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='ProjectName',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='ReverseComplement',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='Sample_ID',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='Sample_Name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='Workflow',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='analysisId',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='group',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='index',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finished_miseq',
            name='refLib',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
