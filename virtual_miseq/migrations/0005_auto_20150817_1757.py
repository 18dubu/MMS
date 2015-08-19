# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_miseq', '0004_experiment_result_folder'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='miseq_folder_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='finish_flag',
            field=models.CharField(default=b'Ongoing', max_length=20, blank=True, choices=[(b'Finished', b'Finished'), (b'Ongoing', b'Ongoing'), (b'Terminated', b'Terminated'), (b'Submitted', b'Submitted'), (b'Analyzing', b'Analyzing'), (b'Rejected', b'Rejected'), (b'Returned', b'Returned'), (b'Closed', b'Closed')]),
        ),
    ]
