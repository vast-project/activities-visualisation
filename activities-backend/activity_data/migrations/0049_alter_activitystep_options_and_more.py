# Generated by Django 5.0.1 on 2024-02-01 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0048_remove_activity_europeana_uriref_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitystep',
            options={'ordering': None},
        ),
        migrations.AlterOrderWithRespectTo(
            name='activitystep',
            order_with_respect_to='activity',
        ),
    ]
