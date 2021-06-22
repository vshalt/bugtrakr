# Generated by Django 3.2.4 on 2021-06-20 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0002_alter_project_users'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('description', models.TextField(blank=True)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], default='', max_length=40)),
                ('status', models.CharField(choices=[('new', 'New'), ('hold', 'On hold'), ('resolved', 'Resolved'), ('waiting', 'Waiting')], default='New', max_length=40)),
                ('classification', models.CharField(choices=[('error', 'Error report'), ('feature', 'Feature request'), ('service', 'Service request'), ('other', 'Other')], default='', max_length=40)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('assigned_users', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assigned', to='accounts.profile')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='owned', to='accounts.profile')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='projects.project')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='TicketHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField(default='')),
                ('ticket', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets.ticket')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.profile')),
            ],
        ),
    ]