# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-22 23:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0007_auto_20161021_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='txccultura',
            name='usuario',
            field=models.ForeignKey(blank=True, db_column='usuario_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='txdpmt',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='pmt/'),
        ),
    ]
