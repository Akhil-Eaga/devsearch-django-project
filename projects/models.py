from django.db import models
import uuid
from users.models import Profile

# Create your models here.
class Project(models.Model):
    # using foreignKey creates a many to one relationship - one profile can have many projects
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL) 
    # SET_NULL will not delete the projects when the profile is deleted
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_count = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        # ordering helps us specify the attributes by which the model instances are ordered
        # by default using the created attribute orders from the oldest to the latest
        # if you use "-created", then the ordering is reversed fromn latest to oldest
        ordering = ['created']


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Upvote'),
        ('down', 'Downvote')
    )
    #owner = # we will add this after creating a user profile 
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 
    # if a project is deleted, then its corresponding reviews will be deleted too
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE) # only two choices for the value column
    created = models.DateTimeField(auto_now_add=True) 
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name