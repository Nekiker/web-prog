from django.db import models
from django.urls import reverse

class PublishStatus(models.IntegerChoices):
    DRAFT = 0, 'Черновик'
    PUBLISHED = 1, 'Опубликовано'

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=PublishStatus.PUBLISHED)

class Starship(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.IntegerField(choices=PublishStatus.choices, default=PublishStatus.PUBLISHED)
    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]