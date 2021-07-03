# Generated by Django 3.2.4 on 2021-07-03 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0013_auto_20210703_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='gmail_id',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='email',
            name='recipients_email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='email',
            name='sender_email',
            field=models.EmailField(max_length=254),
        ),
    ]
