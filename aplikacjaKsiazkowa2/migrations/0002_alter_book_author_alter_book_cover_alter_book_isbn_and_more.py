# Generated by Django 4.0 on 2022-02-04 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplikacjaKsiazkowa2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=200, verbose_name='autor'),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Link do okładki'),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Język'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.IntegerField(blank=True, null=True, verbose_name='Liczba stron'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=200, verbose_name='tytuł'),
        ),
    ]
