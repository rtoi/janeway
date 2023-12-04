# Generated by Django 3.2.18 on 2023-12-04 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('press', '0030_press_secondary_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(blank=True)),
                ('sequence', models.PositiveIntegerField()),
                ('press', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='press.press')),
            ],
            options={
                'ordering': ('sequence',),
            },
        ),
        migrations.CreateModel(
            name='StaffGroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(blank=True, max_length=300)),
                ('alternate_title', models.CharField(blank=True, max_length=300)),
                ('publications', models.TextField(blank=True)),
                ('sequence', models.PositiveIntegerField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='press.staffgroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('sequence',),
            },
        ),
    ]
