# Generated by Django 5.1.2 on 2024-10-31 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_remove_member_role_delete_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='member',
            name='lastname',
        ),
    ]
