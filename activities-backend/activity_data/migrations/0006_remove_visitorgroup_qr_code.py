# Generated by Django 4.0.10 on 2023-05-24 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0005_visitorgroupqrcodes_remove_visitorgroup_frontend_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitorgroup',
            name='qr_code',
        ),
    ]