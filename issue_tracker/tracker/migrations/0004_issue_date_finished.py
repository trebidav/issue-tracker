# Generated by Django 2.0.3 on 2018-03-26 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20180326_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='date_finished',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
