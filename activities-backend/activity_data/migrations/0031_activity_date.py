# Generated by Django 4.2.1 on 2023-06-14 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0030_remove_product_data_remove_statement_context_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]