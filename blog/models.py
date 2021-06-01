from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from taggit.managers import TaggableManager
from django.utils.text import slugify
from ckeditor.fields import RichTextField
# Create your models here.

STATUS_CHOICES = (
    ('RA', 'RECENTLY ADDED'),
    ('MV' , 'MOST WATCHED'),
    ('TR', 'TOP RATED'),

)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='blog/media')
    video_file = models.FileField(blank=True, null=True , default='')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True,max_length=100)
    tags = TaggableManager()
    category = models.CharField(choices=STATUS_CHOICES, max_length=2)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug':self.slug})


    def save(self , *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post , self).save(*args, **kwargs)



#super().save()
#img = Image.open(self.image.path)

#       if img.height > 150 or img.width > 150:
#          output_size = (150 , 150)
 #         img.thumbnail(output_size)
  #        img.save(self.image.path)