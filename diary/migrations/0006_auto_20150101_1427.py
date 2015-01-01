# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0005_auto_20141231_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='edited',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 1, 6, 27, 13, 754126, tzinfo=utc), verbose_name=b'Time Edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 1, 6, 27, 13, 754101, tzinfo=utc), verbose_name=b'Time Published'),
            preserve_default=True,
        ),
    ]
