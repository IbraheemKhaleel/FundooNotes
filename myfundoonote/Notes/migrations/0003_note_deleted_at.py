# Generated by Django 3.1.3 on 2020-12-19 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0002_auto_20201216_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]