# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings
import diary.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diary', '0003_auto_20150107_0223'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempEntryPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_file', models.ImageField(upload_to=diary.models.uuid_filename)),
                ('uploaded', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='entry',
            name='edited',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 19, 21, 57, 34, 60131, tzinfo=utc), verbose_name=b'Time Edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 19, 21, 57, 34, 60091, tzinfo=utc), verbose_name=b'Time Published'),
            preserve_default=True,
        ),
    ]
