# Generated by Django 5.1.6 on 2025-02-07 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, unique=True)),
                ('country_code', models.CharField(blank=True, max_length=10, null=True)),
                ('temperature', models.CharField(blank=True, max_length=10, null=True)),
                ('pressure', models.CharField(blank=True, max_length=10, null=True)),
                ('humidity', models.CharField(blank=True, max_length=10, null=True)),
                ('main', models.CharField(blank=True, max_length=50, null=True)),
                ('icon', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
