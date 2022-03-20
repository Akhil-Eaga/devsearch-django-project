from tkinter import CASCADE
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
        # using a minus sign reverses the ordering (be default is ascending, adding "-" makes it descending)
        # using more than one value to perform ordering means, if there is a tie in ordering based on the first value, 
        # then the second value is used to break the tie and so on and so forth using the subsequent values
        ordering = ["-vote_ratio", "-vote_count", 'title']
        # here the ordering is based on highest vote ratio first and if there is a tie, the highest votes,
        # and if there is a tie even after that, we use alphabetical ordering of the title (note the lack of minus in the title)

    @property
    def reviewers(self):
        # getting a list of reviewers
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        # flat = True does not return a list of tuples, rather a plain list
        # https://stackoverflow.com/questions/37205793/django-values-list-vs-values
        # check the link above to get more clarity on value_list(p) vs values()
        return queryset

    # the @property decorator allows the function to be called as a class property than a function call
    # so to get execute the function, we will say project.updateVoteCount instead of project.updateVoteCount() with the parentheses
    @property
    def updateVoteCount(self):
        # getting all the required values
        reviews = self.review_set.all()
        upVotes = reviews.filter(value="up").count()
        totalVotes = reviews.count()

        # calculating the required values
        voteRatio = int((upVotes / totalVotes) * 100) # calculating the percentage and casting it to integer
        
        # updating the model values
        self.vote_count = totalVotes
        self.vote_ratio = voteRatio

        # saving the updated values
        self.save()


class Review(models.Model):
    # VOTE_TYPE provides a tuple of tuples to use as the only available choices
    # the first element in the inner tuple is for string representation in the admin panel
    # the second element in the inner tuple is for the options shown to the user in dropdown and also in admin panel
    VOTE_TYPE = (
        ('up', 'Upvote'),
        ('down', 'Downvote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True) 
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 
    # if a project is deleted, then its corresponding reviews will be deleted too
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE) # only two choices for the value column
    created = models.DateTimeField(auto_now_add=True) 
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        # this unique_together makes sure that each user (or profile) can only leave one review per project
        # by this condition we are making sure that no user will leave more than one review per project
        # note that unique_together is a list of lists, each inner list is a combination of fields that are unique together
        unique_together = [['owner', 'project']]

    # the def __str__ is basically like the toString method in Java. It overrrides the default string version of any object
    # in java, if we try to print an object, the hexadecimal address of the object gets logged in the console
    # but the toString method helps to give the object a more human readable format of printing or displaying
    # the __str__ in python exactly serves the same purpose
    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name