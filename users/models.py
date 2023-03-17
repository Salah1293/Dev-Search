from email.policy import default

from django.db import models
import uuid
from django.contrib.auth.models import User



class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True,
    upload_to='profiles/', default='profiles/user-default.png')
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_youtube = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def __str__(self):
        return str(self.user.username)


class skill(models.Model):
    owner = models.ForeignKey(profile,on_delete=models.CASCADE, null = True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False,
     unique=True, primary_key=True)
    

    def __str__(self):
        return self.name



class message(models.Model):
    sender = models.ForeignKey(profile,null=True,blank=True, on_delete=models.SET_NULL)
    recipient = models.ForeignKey(profile,null=True,blank=True, on_delete=models.SET_NULL, related_name='messages')
    name = models.CharField(max_length=200 , null=True , blank = True)
    email = models.EmailField(max_length=200 , null=True , blank = True)
    subject = models.CharField(max_length=200 , null=True , blank = True)
    is_read = models.BooleanField(default=False , null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False,
     unique=True, primary_key=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read' , '-created']


    

   