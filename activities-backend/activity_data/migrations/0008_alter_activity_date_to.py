# Generated by Django 4.0.10 on 2023-05-24 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0007_rename_visitorgroupqrcodes_visitorgroupqrcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='date_to',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]