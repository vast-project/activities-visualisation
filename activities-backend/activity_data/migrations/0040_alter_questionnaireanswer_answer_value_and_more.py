# Generated by Django 4.2.5 on 2023-10-21 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0039_alter_visitor_visitors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaireanswer',
            name='answer_value',
            field=models.CharField(blank=True, default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaireanswer',
            name='answer_value_raw',
            field=models.CharField(blank=True, default='', max_length=1024, null=True),
        ),
    ]
