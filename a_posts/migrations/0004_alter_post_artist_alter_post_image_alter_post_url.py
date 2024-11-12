# Generated by Django 5.1.2 on 2024-11-03 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_posts', '0003_alter_post_options_post_artist_post_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='artist',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.URLField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]