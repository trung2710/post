# Generated by Django 5.1.2 on 2024-11-05 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a_posts', '0014_alter_comment_parent_post_alter_reply_parent_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reply',
            options={'ordering': ['-created']},
        ),
    ]
