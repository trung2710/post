# Generated by Django 5.1.2 on 2024-11-06 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_posts', '0017_remove_post_artist_remove_post_url_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='filepost/'),
        ),
    ]
