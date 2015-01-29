# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0007_auto_20150120_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='is_public',
        ),
        migrations.AlterField(
            model_name='entry',
            name='edited',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 20, 16, 30, 23, 493392, tzinfo=utc), verbose_name=b'Time Edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 20, 16, 30, 23, 493355, tzinfo=utc), verbose_name=b'Time Published'),
            preserve_default=True,
        ),
    ]
