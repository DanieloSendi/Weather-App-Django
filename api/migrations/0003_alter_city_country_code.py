# Generated by Django 5.1.6 on 2025-02-08 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_city_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='country_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
