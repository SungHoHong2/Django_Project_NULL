# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 13:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('saytalk', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk_Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('followee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talk_followee', to='saytalk.SayTalk')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talk_follower', to='saytalk.SayTalk')),
            ],
        ),
        migrations.AddField(
            model_name='saytalk',
            name='talk_relation',
            field=models.ManyToManyField(related_name='talk_set_relationship', through='saytalk.Talk_Relationship', to='saytalk.SayTalk'),
        ),
        migrations.AlterUniqueTogether(
            name='talk_relationship',
            unique_together=set([('follower', 'followee')]),
        ),
    ]
