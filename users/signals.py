from pickle import FALSE
from django.db.models.signals import post_save , post_delete
from .models import profile
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail



def createProfile(sender , instance , created , **kwargs):
    if created:
        user= instance
        newProfile = profile.objects.create(
            user = user,
            email = user.email,
            username = user.username,
            name = user.first_name,
        )

def updateUser(sender , instance , created , **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.email = profile.email
        user.username = profile.username
        user.save()

    subject = 'Welcome to Devsearch'
    message = 'We are glad you are here!'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [profile.email],
        fail_silently=False,
    )



def deleteUser(sender , instance , **kwargs):
    user = instance.user
    user.delete()




post_save.connect(createProfile,sender=User)
post_save.connect(updateUser , sender=profile)
post_delete.connect(deleteUser,sender=profile)
