# Generated by Django 5.0.3 on 2024-03-31 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_jsonld_remove_song_json_ld_remove_song_meta_tags_and_more'),
        ('example', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='json_ld',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.jsonld'),
        ),
        migrations.AlterField(
            model_name='car',
            name='meta_tags',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.metatags'),
        ),
        migrations.AlterField(
            model_name='car',
            name='open_graph',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.opengraph'),
        ),
        migrations.AlterField(
            model_name='song',
            name='json_ld',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.jsonld'),
        ),
        migrations.AlterField(
            model_name='song',
            name='seo_content',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.seocontent'),
        ),
        migrations.AlterField(
            model_name='song',
            name='twitter_card',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.twittercard'),
        ),
    ]
