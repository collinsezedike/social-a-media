# Generated by Django 4.1.4 on 2023-01-10 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0002_alter_message_chat_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='chat_id',
            new_name='conversation_id',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='chat_id',
            new_name='conversation_id',
        ),
    ]
