# Generated by Django 4.2.3 on 2023-08-22 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0020_product_document_product_document_resource_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stimulus',
            name='document',
            field=models.FileField(blank=True, default=None, null=True, upload_to='stimulus_documents/'),
        ),
        migrations.AddField(
            model_name='stimulus',
            name='document_resource_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='stimulus',
            name='document_uriref',
            field=models.URLField(blank=True, max_length=512, null=True),
        ),
    ]
