# Generated by Django 5.0.1 on 2024-02-01 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0052_alter_activitystep_step_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitystep',
            options={'ordering': ['step_order']},
        ),
    ]
