# Generated by Django 2.0.2 on 2018-02-12 17:04

from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension

class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_chatmessage_toxicity_score'),
    ]

    operations = [
        TrigramExtension()
    ]
