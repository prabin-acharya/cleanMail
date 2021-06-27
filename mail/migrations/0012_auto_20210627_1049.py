# Generated by Django 3.2.4 on 2021-06-27 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0011_alter_email_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='recipients_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='email',
            name='sender_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
