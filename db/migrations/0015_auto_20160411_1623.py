# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-11 16:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0014_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newstags',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.NewsText'),
        ),
    ]