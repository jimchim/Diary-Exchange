# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import diary.models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_auto_20150107_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='edited',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 6, 18, 23, 15, 487445, tzinfo=utc), verbose_name=b'Time Edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 6, 18, 23, 15, 487399, tzinfo=utc), verbose_name=b'Time Published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entryphoto',
            name='image_file',
            field=models.ImageField(upload_to=diary.models.uuid_filename),
            preserve_default=True,
        ),
    ]
