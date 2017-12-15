# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone
import user_clipboard.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clipboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(max_length=128, upload_to=user_clipboard.models.new_file_upload_to)),
                ('filename', models.CharField(default='', max_length=256, editable=False)),
                ('is_image', models.BooleanField(default=False, db_index=True, editable=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, db_index=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Clipboard Item',
                'verbose_name_plural': 'Clipboard',
            },
        ),
    ]
