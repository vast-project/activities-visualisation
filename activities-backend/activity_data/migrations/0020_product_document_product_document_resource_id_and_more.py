# Generated by Django 4.2.3 on 2023-08-22 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0019_alter_activity_options_alter_activitystep_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='document',
            field=models.FileField(blank=True, default=None, null=True, upload_to='product_documents/'),
        ),
        migrations.AddField(
            model_name='product',
            name='document_resource_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='document_uriref',
            field=models.URLField(blank=True, max_length=512, null=True),
        ),
    ]
