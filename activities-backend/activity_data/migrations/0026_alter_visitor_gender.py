# Generated by Django 4.2.1 on 2023-06-07 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0025_product_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], default=None, max_length=16, null=True),
        ),
    ]