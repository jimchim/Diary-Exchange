# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0008_auto_20150121_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='edited',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Time Edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='published',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Time Published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='slug',
            field=models.SlugField(max_length=180),
            preserve_default=True,
        ),
    ]
