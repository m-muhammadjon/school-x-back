# Generated by Django 4.2.11 on 2024-05-18 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_usertestprogress_userquestionanswer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertestprogress',
            name='duration',
            field=models.DurationField(blank=True, null=True, verbose_name='Duration'),
        ),
    ]
