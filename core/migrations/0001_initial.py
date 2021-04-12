# Generated by Django 3.1.7 on 2021-04-10 09:49

import core.utilities
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('starts_at', models.DateTimeField()),
                ('ends_at', models.DateTimeField()),
                ('region_of_interest', models.FileField(null=True, upload_to='contests/%Y/%m/%d/')),
                ('public_reference_file', models.FileField(blank=True, null=True, upload_to='contests/%Y/%m/%d/')),
                ('private_reference_file', models.FileField(blank=True, null=True, upload_to='contests/%Y/%m/%d/')),
                ('column_to_compare', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.contest')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='On checking', max_length=100)),
                ('file', models.FileField(upload_to=core.utilities.get_attempt_path)),
                ('public_score', models.FloatField(blank=True, null=True)),
                ('private_score', models.FloatField(blank=True, null=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.team')),
            ],
        ),
    ]
