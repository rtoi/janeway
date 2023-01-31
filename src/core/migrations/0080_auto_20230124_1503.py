# Generated by Django 3.2.16 on 2023-01-24 15:03

from django.db import migrations
from django.core.management import call_command


def forwards_func(apps, schema_editor):
    call_command("load_permissions")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0079_auto_20230124_1430'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
            migrations.RunPython.noop,
        ),
    ]