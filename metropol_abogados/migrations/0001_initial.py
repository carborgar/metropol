# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('address', models.CharField(max_length=255, blank=True, null=True)),
                ('location', models.CharField(max_length=255, blank=True, null=True)),
                ('postal_code', models.CharField(max_length=255, blank=True, null=True)),
                ('province', models.CharField(max_length=255, blank=True, null=True)),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='Attendant',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('text_help', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'user_type',
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('description', models.CharField(max_length=255, blank=True, null=True)),
                ('own_attorney', models.BooleanField(db_column='attorney', default=False)),
                ('update_date', models.DateField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'budget',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('text_help', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'event',
            },
        ),
        migrations.CreateModel(
            name='Expedient',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=255, blank=True, null=True)),
                ('creation_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('attendant', models.ForeignKey(db_column='id_user_type', blank=True, to='metropol_abogados.Attendant', null=True)),
            ],
            options={
                'get_latest_by': 'id',
                'ordering': ['-id'],
                'db_table': 'expedient',
            },
        ),
        migrations.CreateModel(
            name='Expiration',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('place', models.CharField(max_length=255, blank=True, null=True)),
                ('date', models.DateTimeField()),
                ('description', models.CharField(max_length=255, blank=True, null=True)),
                ('event', models.ForeignKey(db_column='id_event', blank=True, to='metropol_abogados.Event', null=True)),
                ('expedient', models.ForeignKey(db_column='id_expedient', to='metropol_abogados.Expedient')),
            ],
            options={
                'ordering': ['-date'],
                'db_table': 'expiration',
            },
        ),
        migrations.CreateModel(
            name='ExpPerRol',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('expedient', models.ForeignKey(db_column='id_exp', to='metropol_abogados.Expedient')),
            ],
            options={
                'db_table': 'exp_per_rol',
            },
        ),
        migrations.CreateModel(
            name='Headquarters',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('text_help', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'headquarters',
            },
        ),
        migrations.CreateModel(
            name='LawBranch',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('text_help', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('events', models.ManyToManyField(db_table='branch_event', to='metropol_abogados.Event')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'law_branch',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('expedient', models.ForeignKey(db_column='id_exp', blank=True, to='metropol_abogados.Expedient', null=True)),
            ],
            options={
                'ordering': ['-id'],
                'db_table': 'note',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19)),
                ('budget', models.ForeignKey(db_column='id_budget', blank=True, to='metropol_abogados.Budget', null=True)),
            ],
            options={
                'ordering': ['-date'],
                'db_table': 'payment',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, blank=True, null=True)),
                ('id_number', models.CharField(max_length=255, blank=True, null=True)),
                ('email', models.CharField(max_length=255, blank=True, null=True)),
                ('web', models.CharField(max_length=255, blank=True, null=True)),
                ('nationality', models.CharField(max_length=255, blank=True, null=True)),
                ('creation_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'person',
            },
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('sequence', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('text_help', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('law_branch', models.ForeignKey(db_column='id_law_branch', to='metropol_abogados.LawBranch')),
            ],
            options={
                'ordering': ['sequence'],
                'db_table': 'phase',
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('number', models.CharField(max_length=255)),
                ('person', models.ForeignKey(db_column='id_person', to='metropol_abogados.Person')),
            ],
            options={
                'db_table': 'phone',
            },
        ),
        migrations.CreateModel(
            name='PhoneType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('text_help', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'phone_type',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('text_help', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('text_help', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'state',
            },
        ),
        migrations.CreateModel(
            name='StateBudget',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('text_help', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'state_budget',
            },
        ),
        migrations.AddField(
            model_name='phone',
            name='phone_type',
            field=models.ForeignKey(db_column='id_phone_type', to='metropol_abogados.PhoneType'),
        ),
        migrations.AddField(
            model_name='note',
            name='person',
            field=models.ForeignKey(db_column='id_person', blank=True, to='metropol_abogados.Person', null=True),
        ),
        migrations.AddField(
            model_name='expperrol',
            name='person',
            field=models.ForeignKey(db_column='id_person', to='metropol_abogados.Person'),
        ),
        migrations.AddField(
            model_name='expperrol',
            name='role',
            field=models.ForeignKey(db_column='id_role', to='metropol_abogados.Role'),
        ),
        migrations.AddField(
            model_name='expedient',
            name='headquarters',
            field=models.ForeignKey(db_column='id_headquarters', blank=True, to='metropol_abogados.Headquarters', null=True),
        ),
        migrations.AddField(
            model_name='expedient',
            name='persons',
            field=models.ManyToManyField(through='metropol_abogados.ExpPerRol', to='metropol_abogados.Person'),
        ),
        migrations.AddField(
            model_name='expedient',
            name='phase',
            field=models.ForeignKey(db_column='id_phase', blank=True, to='metropol_abogados.Phase', null=True),
        ),
        migrations.AddField(
            model_name='expedient',
            name='state',
            field=models.ForeignKey(db_column='id_state', to='metropol_abogados.State'),
        ),
        migrations.AddField(
            model_name='budget',
            name='expedient',
            field=models.OneToOneField(db_column='id_expedient', blank=True, to='metropol_abogados.Expedient', null=True),
        ),
        migrations.AddField(
            model_name='budget',
            name='state_budget',
            field=models.ForeignKey(db_column='id_state_budget', blank=True, to='metropol_abogados.StateBudget', null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='person',
            field=models.ForeignKey(db_column='id_person', to='metropol_abogados.Person'),
        ),
        migrations.AlterUniqueTogether(
            name='phase',
            unique_together=set([('id', 'sequence')]),
        ),
        migrations.AlterUniqueTogether(
            name='expperrol',
            unique_together=set([('person', 'role', 'expedient')]),
        ),
    ]
