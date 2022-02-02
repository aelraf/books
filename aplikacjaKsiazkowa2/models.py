# -*- coding: utf-8 -*-

from django.db import models


class Book(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    pub_date = models.DateField('data publikacji', blank=True, null=True)
    isbn = models.CharField(max_length=15, null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    cover = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.title + " - " + self.author

    class Meta:
        ordering = ['id']

