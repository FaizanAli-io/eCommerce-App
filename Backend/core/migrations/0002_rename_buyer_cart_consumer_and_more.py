# Generated by Django 5.0.1 on 2024-02-13 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='buyer',
            new_name='consumer',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='buyer',
            new_name='consumer',
        ),
    ]
