# Generated by Django 4.2.5 on 2023-10-10 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0038_virtualvisitor_visitor_visitors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='visitors',
            field=models.ManyToManyField(blank=True, default=None, to='activity_data.visitor'),
        ),
    ]