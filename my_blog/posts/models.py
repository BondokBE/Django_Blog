import random

from datetime import datetime, timedelta
from markdown_deux import markdown

from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from .utils import get_read_time, random_string_generator

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Note! : Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(publish__lte=timezone.now())


def upload_location(post, file_name):
    return "{}/{}".format(post.id, file_name)


class Post(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title           = models.CharField(max_length=128)
    slug            = models.SlugField()
    width_field     = models.IntegerField(default=0)
    height_field    = models.IntegerField(default=0)
    content         = models.TextField() 
    publish         = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now())
    updated         = models.DateTimeField(auto_now=True, auto_now_add=False)
    time_stamp      = models.DateTimeField(auto_now=False, auto_now_add=True)
    time_now        = datetime.now()
    image           = models.ImageField(
                upload_to=upload_location, 
                null=True, 
                blank=True, 
                width_field="width_field", 
                height_field="height_field",
    )

    read_time = models.IntegerField(default=0)
    # read_time = get_read_time(content)

    objects = PostManager()
    # to return post title as object name, instead "Post object"
    def __str__(self):
        return self.title
        
    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def get_absolute_url(self):
        # return "/posts/%s/" %(self.slug) 
        # ^ it's not fully dynamic, it works with {{ post.get_absolute_url }} inside the post.html
        return reverse("posts:post", kwargs={'slug': self.slug})  # to reverse and make even more dynamic

    def edit_url(self):
        return reverse("posts:edit", kwargs={'slug': self.slug})
    
    def delete_url(self):
        return reverse("posts:delete", kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-time_stamp', '-updated']

    # simple slug generator

    def save(self, *args, **kwargs):
        # slugify title
        # self.slug = slugify("{obj.product_name}-{obj.id}".format(obj=self))
        size = random.randint(5, 9)
        self.slug = slugify("{slug}-{rand_str}".format(slug=self.title, rand_str=random_string_generator(size=size)))
        # read time auto-generated
        self.read_time = get_read_time(self.content)
        
        super(Post, self).save(*args, **kwargs)

