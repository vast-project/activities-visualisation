# Generated by Django 4.2.5 on 2023-10-02 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0033_alter_stimulus_stimulus_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
