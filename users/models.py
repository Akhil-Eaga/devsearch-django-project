from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Profile(models.Model):
    # everytime a user is deleted, its corresponding profile will be deleted too
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="profiles/", default="profiles/user-default.png")

    # social media links
    social_github = models.CharField(max_length=500, null=True, blank=True)
    social_stackoverflow = models.CharField(max_length=500, null=True, blank=True)
    social_twitter = models.CharField(max_length=500, null=True, blank=True)
    social_linkedin = models.CharField(max_length=500, null=True, blank=True)
    social_youtube = models.CharField(max_length=500, null=True, blank=True)
    social_website = models.CharField(max_length=500, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        # if you happen to use a number field for the string representation, then make sure to cast to string
        return str(self.username)


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Message(models.Model):
    # sender is the person sending the message
    # sender does not need to have a user account with devsearch to send a message, hence the null = True and blank = True
    # if a sender deletes their profile, the recipient should still be able to see the messages, hence the models.SET_NULL
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)

    # recipient is the person receiving the message
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    # django DOES NOT allow us to have two fields that access the same foreign key, so we need to have 
    # atleast one of those fields to have a related_name attribute and this will solve that issue
    # related_name helps us in accessing the property somewhat differently
    # without a related name, we use the profile.message_set.all()
    # with a related name, we use profile.messages(), assuming that the related name is "messages"
    
    # we want a name regardless of the sender having a user account or not
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(max_length=1000, null=True) # we dont a blank message, so did not set blank=True
    is_read = models.BooleanField(default=False, null=True) # represents whether the message is read or not
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    # explanation for null = True and blank = True and their differences
    # https://stackoverflow.com/questions/8609192/what-is-the-difference-between-null-true-and-blank-true-in-django

    def __str__(self):
        return self.subject

    # ordering the messages by unread messages first and within the unread or read messages we use latest to oldest order for messages
    class Meta:
        ordering = ['is_read', '-created']
    