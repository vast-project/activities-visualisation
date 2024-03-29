# Generated by Django 4.2.3 on 2023-08-08 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0002_alter_visitorgroupqrcode_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorgroupqrcode',
            name='qr_code',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='qr_codes'),
        ),
        migrations.AlterField(
            model_name='visitorgroupqrcode',
            name='uriref',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
