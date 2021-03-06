# Generated by Django 3.2.4 on 2021-07-01 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_rename_assigned_users_ticket_assigned_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], default='', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('hold', 'On hold'), ('resolved', 'Resolved'), ('waiting', 'Waiting')], default='new', max_length=40),
        ),
    ]
