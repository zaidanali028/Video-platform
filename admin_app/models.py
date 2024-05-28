from django.db import models

from  django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class User(AbstractUser):
    
    USERNAME_FIELD = "email"
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=255,null=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    brand_name = models.CharField(max_length=255, unique=True, null=True)
    profile_image_url = models.URLField(max_length=255, blank=True, null=True)

    REQUIRED_FIELDS=[]


class Category(models.Model):
    class Meta:
          ordering=['-updated_at','created_at']
        #   all currently updated records should come first or default-behaviour, order it in ascending order by the ones currently created
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
     ]
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Genre(models.Model):
    class Meta:
          ordering=['-updated_at','created_at']
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
     ]
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Video(models.Model):
    class Meta:
          ordering=['-updated_at','created_at']
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
     ]
    title = models.CharField(max_length=255,unique=True,blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='videos_set')
    genres = models.ManyToManyField(Genre, related_name='videos_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    thumb_image_url = models.URLField(max_length=255, blank=True, null=True)
    video_url = models.URLField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)  
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.title