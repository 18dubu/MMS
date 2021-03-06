# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CcleLibrary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CCLE_name', models.CharField(default=b'', max_length=64, verbose_name=b'CCLE Name')),
                ('Cell_line_primary_name', models.CharField(max_length=150, null=True, verbose_name=b'Cell Line Primary Name')),
                ('Cell_line_aliases', models.CharField(max_length=150, null=True, verbose_name=b'Cell Line Aliases')),
                ('Disease_Area', models.CharField(default=b'Oncology', max_length=150, null=True, verbose_name=b'Disease Area')),
                ('Gender', models.CharField(default=b'U', max_length=5, verbose_name=b'Gender', choices=[(b'M', b'M'), (b'F', b'F'), (b'U', b'U')])),
                ('Site_Primary', models.CharField(max_length=64, null=True, verbose_name=b'Site Primary')),
                ('Histology', models.CharField(max_length=64, null=True, verbose_name=b'Histology')),
                ('Hist_Subtype1', models.CharField(max_length=64, null=True, verbose_name=b'Hist Subtype')),
                ('Notes', models.TextField(verbose_name=b'Note')),
                ('Source', models.CharField(max_length=32, null=True, verbose_name=b'Source')),
                ('approvalStatus', models.BooleanField(default=True, choices=[(True, b'Approved'), (False, b'Pending')])),
            ],
        ),
        migrations.CreateModel(
            name='CellModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, null=True, verbose_name=b'Name')),
                ('parent', models.CharField(max_length=100, null=True, verbose_name=b'Parent')),
                ('source', models.CharField(max_length=45, null=True, verbose_name=b'Source')),
                ('catalog_number', models.CharField(max_length=155, null=True, verbose_name=b'Catalog number')),
                ('species', models.CharField(max_length=45, null=True, verbose_name=b'Species')),
                ('ccle_name', models.CharField(max_length=100, null=True, verbose_name=b'Ccle name')),
                ('tissue', models.CharField(max_length=100, null=True, verbose_name=b'Tissue')),
                ('cell_type', models.CharField(max_length=100, null=True, verbose_name=b'Cell type')),
                ('disease', models.CharField(max_length=100, null=True, verbose_name=b'Disease')),
                ('histopath', models.CharField(max_length=150, null=True, verbose_name=b'Histopath')),
                ('gender', models.CharField(max_length=10, null=True, verbose_name=b'Gender')),
                ('engineering', models.CharField(max_length=150, null=True, verbose_name=b'Engineering')),
                ('selection', models.CharField(max_length=100, null=True, verbose_name=b'Selection')),
                ('validated', models.CharField(max_length=20, null=True, verbose_name=b'Validated')),
                ('str_mod', models.TextField()),
                ('isoenzymes', models.CharField(max_length=45, null=True, verbose_name=b'Isoenzymes')),
                ('map_tested', models.CharField(max_length=45, null=True, verbose_name=b'Map tested')),
                ('invivo_growth', models.CharField(max_length=45, null=True, verbose_name=b'Invivo growth')),
                ('culture_medium', models.CharField(max_length=155, null=True, verbose_name=b'Culture medium')),
                ('subculturing', models.TextField()),
                ('doubling', models.CharField(max_length=45, null=True, verbose_name=b'Doubling')),
                ('commercial_link', models.CharField(max_length=255, null=True, verbose_name=b'Commercial Link')),
                ('location', models.CharField(max_length=150, null=True, verbose_name=b'Location')),
                ('submitter', models.CharField(max_length=100, null=True, verbose_name=b'Submitter')),
                ('date', models.CharField(max_length=45, null=True, verbose_name=b'Date')),
                ('comments', models.TextField()),
                ('freezerpro_id', models.IntegerField(null=True, verbose_name=b'Freezerpro ID')),
                ('approvalStatus', models.BooleanField(default=True, choices=[(True, b'Approved'), (False, b'Pending')])),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('experiment_id', models.CharField(default=uuid.uuid4, unique=True, max_length=200, blank=True)),
                ('project_name', models.CharField(default=b'', max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('experiment_date', models.DateTimeField(verbose_name=b'Date of experiment')),
                ('disease_area', models.CharField(default=b'oncology', max_length=50, null=True, verbose_name=b'Disease Area', choices=[(b'oncology', b'oncology')])),
                ('workflow', models.CharField(default=b'GenerateFASTQ', max_length=200)),
                ('chemistry', models.CharField(default=b'26DCx21x7', max_length=200)),
                ('application', models.CharField(default=b'FASTQ Only', max_length=200)),
                ('assay', models.CharField(default=b'TruSeq LT', max_length=200)),
                ('version', models.PositiveSmallIntegerField(default=4)),
                ('reads', models.BigIntegerField(default=21)),
                ('design_type', models.CharField(max_length=200, null=True, blank=True)),
                ('reverse_complement', models.IntegerField(default=0, null=True, verbose_name=b'Reverse Complement')),
                ('feedback_flag', models.NullBooleanField()),
                ('comment', models.CharField(max_length=200, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Created Date', blank=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name=b'Updated date', null=True)),
                ('download_date', models.DateTimeField(null=True, verbose_name=b'Download Date', blank=True)),
                ('finish_flag', models.CharField(default=b'Ongoing', max_length=20, blank=True, choices=[(b'Finished', b'Finished'), (b'Ongoing', b'Ongoing'), (b'Terminated', b'Terminated')])),
            ],
        ),
        migrations.CreateModel(
            name='IDMSUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('UserID', models.IntegerField(default=0, verbose_name=b'User ID')),
                ('Username', models.CharField(default=b'', max_length=255, verbose_name=b'User Name')),
                ('Password', models.CharField(default=b'', max_length=32, verbose_name=b'Password')),
                ('EmailAddress', models.EmailField(default=b'test@test.com', max_length=255, verbose_name=b'Email Address')),
                ('FirstName', models.CharField(default=b'', max_length=65, verbose_name=b'First Name')),
                ('LastName', models.CharField(default=b'', max_length=65, verbose_name=b'Last Name')),
                ('Phone', models.CharField(default=b'', max_length=20, verbose_name=b'Phone')),
                ('Privilege', models.CharField(default=b'c', max_length=10, verbose_name=b'Privilege', choices=[(b's', b's'), (b'i', b'i'), (b'a', b'a'), (b'b', b'b'), (b'c', b'c'), (b'f', b'f'), (b'g', b'g'), (b'o', b'o'), (b'x', b'x'), (b'y', b'y'), (b'z', b'z')])),
                ('ValidationStatus', models.CharField(default=b'pending', max_length=30, verbose_name=b'Validation Status')),
                ('AuthenticationString', models.CharField(default=b'', max_length=20, verbose_name=b'Authentication String')),
                ('user_group', models.CharField(default=b'', max_length=30, verbose_name=b'User Group')),
                ('Organization', models.CharField(default=b'Oncology Research', max_length=45, verbose_name=b'Organization')),
                ('Billingaddress', models.CharField(max_length=150, null=True, verbose_name=b'Billing Address')),
                ('Billingcity', models.CharField(max_length=100, null=True, verbose_name=b'Billing City')),
                ('Billingstate', models.CharField(max_length=20, null=True, verbose_name=b'Billing State')),
                ('Billingzip', models.IntegerField(null=True, verbose_name=b'Billin ZIP')),
                ('Shippingaddress', models.CharField(max_length=150, null=True, verbose_name=b'Shipping Adress')),
                ('Shippingbuilding', models.CharField(max_length=100, null=True, verbose_name=b'Shipping Building')),
                ('Shippingroom', models.CharField(max_length=45, null=True, verbose_name=b'Shipping Room')),
                ('Shippingcity', models.CharField(max_length=100, null=True, verbose_name=b'Shipping City')),
                ('Shippingstate', models.CharField(max_length=20, null=True, verbose_name=b'Shipping State')),
                ('Shippingzip', models.IntegerField(null=True, verbose_name=b'Shipping ZIP')),
                ('NTID', models.CharField(max_length=20, null=True, verbose_name=b'NTID')),
                ('approvalStatus', models.BooleanField(default=True, choices=[(True, b'Approved'), (False, b'Pending')])),
            ],
        ),
        migrations.CreateModel(
            name='MiseqIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('I7_Index_ID', models.CharField(max_length=32, verbose_name=b'I7 Index')),
                ('index', models.CharField(max_length=32, verbose_name=b'MiSeq Index')),
                ('approvalStatus', models.BooleanField(default=True, choices=[(True, b'Approved'), (False, b'Pending')])),
            ],
        ),
        migrations.CreateModel(
            name='PoolNumberChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=300)),
                ('approvalStatus', models.BooleanField(default=True, choices=[(True, b'Approved'), (False, b'Pending')])),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sample_id', models.IntegerField(null=True, blank=True)),
                ('shRNA_on', models.BooleanField(choices=[(True, b'ON'), (False, b'OFF')])),
                ('time_in_days', models.PositiveSmallIntegerField()),
                ('treatment_dose', models.IntegerField(null=True, blank=True)),
                ('replicate', models.CharField(max_length=5, null=True, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C'), (b'D', b'D'), (b'E', b'E'), (b'F', b'F'), (b'G', b'G'), (b'H', b'H'), (b'I', b'I'), (b'J', b'J'), (b'K', b'K'), (b'L', b'L'), (b'M', b'M'), (b'N', b'N'), (b'O', b'O'), (b'P', b'P'), (b'Q', b'Q'), (b'R', b'R'), (b'S', b'S'), (b'T', b'T'), (b'U', b'U'), (b'V', b'V'), (b'W', b'W'), (b'X', b'X'), (b'Y', b'Y'), (b'Z', b'Z')])),
                ('feedback_flag', models.NullBooleanField()),
                ('finish_flag', models.CharField(default=b'Ongoing', max_length=20, blank=True, choices=[(b'Finished', b'Finished'), (b'Ongoing', b'Ongoing'), (b'Terminated', b'Terminated')])),
                ('other_tag', models.CharField(max_length=200, null=True, blank=True)),
                ('comment', models.CharField(max_length=200, null=True, blank=True)),
                ('sample_name', models.CharField(max_length=200, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Created Date', blank=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name=b'Updated date', null=True)),
                ('download_date', models.DateTimeField(null=True, verbose_name=b'Download Date', blank=True)),
                ('cell_model', models.ForeignKey(related_name='cell_model', to='virtual_miseq.CcleLibrary', null=True)),
                ('created_by', models.ForeignKey(related_name='sample_created_by', blank=True, to='virtual_miseq.IDMSUser', null=True)),
                ('download_by', models.ManyToManyField(related_name='sample_download_by', to='virtual_miseq.IDMSUser', blank=True)),
                ('experiment', models.ForeignKey(blank=True, to='virtual_miseq.Experiment', null=True)),
                ('index', models.ForeignKey(related_name='miseqIndex_index', to='virtual_miseq.MiseqIndex', null=True)),
                ('pool_number', models.ManyToManyField(related_name='sample_pool_number', to='virtual_miseq.PoolNumberChoice', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShrnaLibrary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('LibName', models.CharField(default=b'', max_length=256, verbose_name=b'Library Name')),
                ('LibName_Full', models.CharField(default=b'', max_length=256, verbose_name=b'Library Full Name')),
                ('Description', models.TextField()),
                ('Source', models.CharField(default=b'', max_length=256, verbose_name=b'Source')),
                ('Num_Pools', models.IntegerField(null=True, verbose_name=b'Number of Pools')),
                ('CreationDate', models.CharField(max_length=256, null=True, verbose_name=b'Creation Date')),
                ('Num_shRNAs', models.IntegerField(null=True, verbose_name=b'Number of shRNAs')),
                ('Num_Genes', models.IntegerField(null=True, verbose_name=b'Number of genes')),
                ('Num_shRNAsPerGene', models.IntegerField(null=True, verbose_name=b'Number of shRNAs per gene')),
                ('AnnotationFile', models.CharField(default=b'', max_length=512, verbose_name=b'Annotation File')),
                ('DNAStringSet_Object', models.CharField(default=b'', max_length=512, verbose_name=b'DNAStringSet_Object')),
                ('approvalStatus', models.BooleanField(default=True, choices=[(True, b'Approved'), (False, b'Pending')])),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('compoundName', models.CharField(max_length=64, verbose_name=b'Compound Name')),
                ('CompoundFullName', models.CharField(max_length=256, verbose_name=b'CompoundFullName')),
                ('PfizerNumber', models.CharField(max_length=32, verbose_name=b'Pfizer Number')),
                ('Description', models.CharField(max_length=256, verbose_name=b'Description')),
                ('Source', models.CharField(max_length=256, verbose_name=b'Source')),
                ('Investigator', models.CharField(max_length=32, verbose_name=b'Investigator')),
                ('approvalStatus', models.BooleanField(default=True, choices=[(True, b'Approved'), (False, b'Pending')])),
            ],
        ),
        migrations.CreateModel(
            name='VectorLibrary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, null=True, verbose_name=b'Name')),
                ('shortname', models.IntegerField(null=True, verbose_name=b'Short Name')),
                ('vector_backbone', models.CharField(max_length=150, null=True, verbose_name=b'Vector Backbone')),
                ('submitter', models.CharField(max_length=45, null=True, verbose_name=b'Submitter')),
                ('department', models.CharField(max_length=100, null=True, verbose_name=b'Department')),
                ('type_mod', models.CharField(max_length=150, null=True, verbose_name=b'Type')),
                ('application', models.CharField(max_length=150, null=True, verbose_name=b'application')),
                ('promoter', models.CharField(max_length=150, null=True, verbose_name=b'Promoter')),
                ('gene', models.CharField(max_length=150, null=True, verbose_name=b'Gene')),
                ('insert_origin', models.CharField(max_length=45, null=True, verbose_name=b'Insert origin')),
                ('bacterial_selection', models.CharField(max_length=45, null=True, verbose_name=b'Bacterial Selection')),
                ('other_selection', models.CharField(max_length=45, null=True, verbose_name=b'Other Selection')),
                ('reporter', models.CharField(max_length=45, null=True, verbose_name=b'Reporter')),
                ('dot_clone', models.CharField(max_length=45, null=True, verbose_name=b'Dot clone')),
                ('bacterial_stock', models.CharField(max_length=45, null=True, verbose_name=b'Bacterial stock')),
                ('bacterial_stock_type', models.CharField(max_length=45, null=True, verbose_name=b'Bacterial stock type')),
                ('bacterial_stock_location', models.TextField()),
                ('plasmid_dna_location', models.TextField()),
                ('plasmid_concentration', models.CharField(max_length=45, null=True, verbose_name=b'Plasmid concentration')),
                ('vector_seq', models.TextField(verbose_name=b'Vector seq')),
                ('insert_seq', models.TextField(verbose_name=b'Insert seq')),
                ('upstream_atg', models.CharField(max_length=45, null=True, verbose_name=b'Upstream atg')),
                ('validations', models.TextField(verbose_name=b'Validations')),
                ('hash_mod', models.CharField(max_length=64, null=True, verbose_name=b'Hash')),
                ('creation_date', models.DateField(null=True, verbose_name=b'Creation date')),
                ('comments', models.TextField(verbose_name=b'Comments')),
                ('insert_accession', models.CharField(max_length=45, null=True, verbose_name=b'Insert accession')),
                ('transcript', models.TextField(verbose_name=b'Transcript')),
                ('protein', models.TextField(verbose_name=b'Protein')),
                ('orf', models.TextField(verbose_name=b'Orf')),
                ('approvalStatus', models.BooleanField(default=True, choices=[(True, b'Approved'), (False, b'Pending')])),
            ],
        ),
        migrations.AddField(
            model_name='shrnalibrary',
            name='Vector',
            field=models.ForeignKey(related_name='vector_shortname', blank=True, to='virtual_miseq.VectorLibrary', null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='shRNA_library',
            field=models.ForeignKey(related_name='shRNA_LibName', to='virtual_miseq.ShrnaLibrary', null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='treatment',
            field=models.ForeignKey(related_name='treatment_compoundName', blank=True, to='virtual_miseq.Treatment', null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='updated_by',
            field=models.ManyToManyField(related_name='sample_updated_by', to='virtual_miseq.IDMSUser', blank=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='created_by',
            field=models.ForeignKey(related_name='exp_created_by', blank=True, to='virtual_miseq.IDMSUser', null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='download_by',
            field=models.ManyToManyField(related_name='exp_download_by', to='virtual_miseq.IDMSUser', blank=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='investigator',
            field=models.ManyToManyField(related_name='investigator', to='virtual_miseq.IDMSUser'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='updated_by',
            field=models.ManyToManyField(related_name='exp_updated_by', to='virtual_miseq.IDMSUser', blank=True),
        ),
    ]
