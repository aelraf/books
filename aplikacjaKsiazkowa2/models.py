# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Book(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    pub_date = models.DateField('data publikacji')
    isbn = models.CharField(max_length=15, null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    cover = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.title + " - " + self.author

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta:
        ordering = ['id']

"""
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='author_headshots')
    last_accessed = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})
"""
