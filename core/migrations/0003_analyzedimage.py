# Generated by Django 5.0.3 on 2024-03-30 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_song_twitter_card_song_meta_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyzedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('alt', models.CharField(max_length=125, null=True)),
                ('json_ld', models.JSONField(null=True)),
            ],
        ),
    ]
