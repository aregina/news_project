# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-06 05:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('url', models.CharField(max_length=300)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('summary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RssChannels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='rsschannels',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Site'),
        ),
        migrations.AddField(
            model_name='news',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Site'),
        ),
    ]
