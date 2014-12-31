# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0003_auto_20141231_0234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='author',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='edited',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 30, 18, 56, 46, 365769, tzinfo=utc), verbose_name=b'Time Edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 30, 18, 56, 46, 365739, tzinfo=utc), verbose_name=b'Time Published'),
            preserve_default=True,
        ),
    ]
