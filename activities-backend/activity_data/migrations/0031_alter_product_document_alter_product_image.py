# Generated by Django 4.2.3 on 2023-09-08 17:01

import activity_data.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0030_alter_stimulus_document_alter_stimulus_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='document',
            field=models.FileField(blank=True, default=None, null=True, upload_to=activity_data.models.Product_remove_spaces_from_filename),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=activity_data.models.Product_remove_spaces_from_image_filename),
        ),
    ]
