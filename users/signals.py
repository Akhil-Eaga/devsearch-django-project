from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

from django.conf import settings
from django.core.mail import send_mail

# -------------- THIS IS ONE WAY OF CONNECTING RECEIVERS TO THE SIGNALS ---------------------


# the @receiver decorator makes the function a receiver function
# this means that our profileUpdated method will run after (post_save) a Profile is saved
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )


        # THIS IS SUPPOSED TO WORK BUT NOT WORKING - NOT SURE WHY - MOSTLY BECAUSE OF THE GOOGLE SMTP SETTINGS
        # sending a welcome email everytime a user account is created
        # subject = "Welcome to DevSearch"
        # message = "We are glad you are here. Thank you !!!"
        # send_mail(
        #     subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [profile.email],
        #     fail_silently=False,
        # )


@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        # this block is updating an existing user object
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

# this menas that our deleteUser method will run after (post_delete) a Profile is deleted


@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    # since the instance here is of type profile, to get the user, we can do instance.user
    user = instance.user
    user.delete()


# -------------- THIS IS ANOTHER WAY OF CONNECTING RECEIVERS TO THE SIGNALS ---------------------
# # this function is the receiver of the signal
# # param sender: it is the model that actually sends the signal
# # param instance: instance of the model that actually triggered the signal
# # param created: this is just a boolean value representing the model was created or just saved again
# # param created basically tells us whether a new record in the db has been added or not
# def profileUpdated(sender, instance, created, **kwargs):
#     print("Profile saved !!!!!")
#     print("Sender ", sender)
#     print('Instance ', instance)
#     print('Created ', created)


# def deleteUser(sender, instance, **kwargs):
#     print("Profile deleted !!!!!")
#     print("Sender ", sender)
#     print('Instance ', instance)

# # now we want to connect the receiver method to the post_save method within the signal
# # the sender param is representing what model triggers the signal (in our case, its the Profile model)
# post_save.connect(profileUpdated, sender=Profile)

# post_delete.connect(deleteUser, sender=Profile)
