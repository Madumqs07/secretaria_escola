# Generated by Django 5.2 on 2025-04-09 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secretaria', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='turma',
            old_name='class_choice',
            new_name='escolha_a_turma',
        ),
    ]
