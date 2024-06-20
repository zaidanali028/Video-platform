from django.db import models

from  django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class User(AbstractUser):
    # pass
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=255,null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    brand_name = models.CharField(max_length=255, unique=False, null=True)
    brand_image_url = models.URLField(max_length=255, blank=True, null=True)
   
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]
    #overriding the username_field to take email instead of username and making the required_fields empty 
      

        
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
        self.name=self.name.capitalize()
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    


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
        self.name=self.name.capitalize()
        
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class Show(models.Model):
    class Meta:
        ordering=['-updated_at','created_at']
    STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ]
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_image_url = models.URLField(max_length=200, blank=True, null=True)
    view_count = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name='categories_set')
    genres = models.ManyToManyField(Genre, related_name='genres_set')
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.title=self.title.capitalize()
        
        super(Show, self).save(*args, **kwargs)

    def __str__(self):
        return self.title




class Video(models.Model):
    # class Meta:
        #   ordering=['-updated_at','created_at']
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
     ]
    title = models.CharField(max_length=255,unique=True,blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    thumb_image_url = models.URLField(max_length=255, blank=True, null=True)
    video_url = models.URLField(max_length=255, blank=True, null=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, default=None)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)  
        self.title=self.title.capitalize()
        
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
