# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0004_auto_20150120_0557'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tempentryphoto',
            old_name='uploaded',
            new_name='uploader',
        ),
        migrations.AlterField(
            model_name='entry',
            name='edited',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 19, 22, 11, 53, 423745, tzinfo=utc), verbose_name=b'Time Edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 19, 22, 11, 53, 423700, tzinfo=utc), verbose_name=b'Time Published'),
            preserve_default=True,
        ),
    ]
