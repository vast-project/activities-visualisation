# Generated by Django 5.0.1 on 2024-02-01 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0049_alter_activitystep_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitystep',
            name='step_order',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]