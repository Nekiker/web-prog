from django.db import models
from django.urls import reverse

class PublishStatus(models.IntegerChoices):
    DRAFT = 0, 'Черновик'
    PUBLISHED = 1, 'Опубликовано'

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=PublishStatus.PUBLISHED)

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

class ShipPassport(models.Model):
    reg_number = models.CharField(max_length=50, unique=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f"{self.reg_number}"


class Starship(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.IntegerField(choices=PublishStatus.choices, default=PublishStatus.PUBLISHED)
    objects = models.Manager()
    published = PublishedManager()
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')
    passport = models.OneToOneField('ShipPassport', on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='starship')

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]