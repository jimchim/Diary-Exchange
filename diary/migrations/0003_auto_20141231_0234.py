# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_auto_20141231_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='edited',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 30, 18, 34, 51, 434054, tzinfo=utc), verbose_name=b'Time Edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 30, 18, 34, 51, 434025, tzinfo=utc), verbose_name=b'Time Published'),
            preserve_default=True,
        ),
    ]
