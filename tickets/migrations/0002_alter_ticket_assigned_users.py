# Generated by Django 3.2.4 on 2021-06-21 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='assigned_users',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='assigned', to='accounts.profile'),
        ),
    ]
