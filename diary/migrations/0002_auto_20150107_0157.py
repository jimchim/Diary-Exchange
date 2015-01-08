# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='edited',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 6, 17, 57, 21, 421335, tzinfo=utc), verbose_name=b'Time Edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 6, 17, 57, 21, 421304, tzinfo=utc), verbose_name=b'Time Published'),
            preserve_default=True,
        ),
    ]
