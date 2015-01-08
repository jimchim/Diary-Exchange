# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=180)),
                ('body', models.TextField()),
                ('slug', models.SlugField()),
                ('published', models.DateTimeField(default=datetime.datetime(2015, 1, 6, 17, 56, 57, 839466, tzinfo=utc), verbose_name=b'Time Published')),
                ('edited', models.DateTimeField(default=datetime.datetime(2015, 1, 6, 17, 56, 57, 839505, tzinfo=utc), verbose_name=b'Time Edited')),
                ('is_draft', models.BooleanField(default=True)),
                ('is_public', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_file', models.ImageField(upload_to=b'entry_photo')),
                ('article', models.ForeignKey(to='diary.Entry')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
