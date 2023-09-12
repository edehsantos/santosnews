from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image



class News_Category(models.Model):
    title = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    
    
    class Meta:
        ordering = ['-title']
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.title
    
    
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    description = models.TextField()
    image_user = models.ImageField(upload_to='authors_images')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  
    
    def __str__(self):
        return str(self.user)  
    
    
    
class Post(models.Model):
    class STATUS(models.TextChoices):
        DRAFT = 'DF', 'Draft',
        PUBLISHED = 'PB', 'publish'
    category = models.ForeignKey(News_Category, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='authors')
    title = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=256, db_index=True, unique_for_date='publish')
    images = models.ImageField(upload_to='post_images')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)    
    status = models.CharField(max_length=2, choices=STATUS.choices, default=STATUS.DRAFT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    
    tags = TaggableManager()
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        image = Image.open(self.images.path)
        
        desired_width = 900
        desired_height = 800
        
        image = image.resize((desired_width, desired_height), Image.ANTIALIAS)
        image.save(self.images.path)
        
        
    
    
    def get_absolute_url(self):
        return reverse("post_details", args=[self.id, self.slug, self.publish.year, self.publish.month, self.publish.day])
    
    
    
    class Meta:
        ordering = ['-title']
        
        
class Comment(models.Model):
    name = models.CharField(max_length=250)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"    
    
    
class Message(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    email = models.EmailField()
    subject = models.CharField(max_length=256)
    message = models.TextField()
    
    def __str__(self):
        return f"{self.message} by {self.name} on {self.email}"     
            