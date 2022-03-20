from email import message
from re import search
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .utils import paginateProfiles, searchProfiles
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm

# Create your views here.


def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        # we can use the bracket notation to access the form field values
        username = request.POST['username'].lower()
        # or we can alternatively use the .get method to access the form field values 
        password = request.POST.get('password')

        try:
            # checking if the username exists in the db or not
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")
            return redirect('login')

        # user will be None if the authenticate function cannot validate the username against the password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # logging in the user
            login(request, user)
            # to redirect the users to the page they were previously on, 
            # we will check for the "next" query parameter in the request.GET else redirect to "account"

            # NOTE: Although we are inside the request.POST if block, we can still get access to the request.GET
            # because we made the action = "" (basically empty action) in the jinja template form 
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            # at this point, we have validated the user exists but the password did not actually match
            messages.error(request, "Username or password is incorrect")

    context = {'page': page}
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('login')


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    # requst.user returns the current user
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # commit = False actually holds a temporary instance of the user before actually saving it to the db
            # in this context, we are using it to do some additional processing on the data before saving it to db
            # this same result can be achieved using the forms itself but this is done to demonstrate the commit = False
            user.username = user.username.lower()
            # to save the processed data
            user.save()
            messages.success(request, "User account was created successfully")
            # .success after the messages represent the tag type and can be used to apply conditional styles as shown in the main.html

            # after successful registration, login the user and redirect them to the profiles page
            login(request, user)
            return redirect('edit-account')

        # else:
        #     messages.error(request, "An error has occured during registration")

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request)
    
    results_per_page = 3

    custom_range, profiles, paginator = paginateProfiles(request, profiles, results_per_page)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
        'paginator': paginator
    }
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    # .exclude method here outputs skills that has a description
    topSkills = profile.skill_set.exclude(description__exact="")
    # .filter method here outputs skills that does not have a description
    otherSkills = profile.skill_set.filter(description="")
    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills
    }
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        # the instance tells us which profile we are updating
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Added new skill")

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)

        if form.is_valid():
            form.save()
            messages.success(request, "Updated the skill")
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


# since delete_template.html is in the main project templates directory, it can be used in any app within the project
# reason for keeping the delete_template.html in the main templates directory is because the delete functionality template can be reused
# using modals would be a good idea to add more polish to the application UX

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Deleted the skill")
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    # currently logged in user
    profile = request.user.profile

    # make sure to name this variable anything other than messages, because our flash messages import uses the name "messages"
    messageRequests = profile.messages.all()
    # the reason why we used messages.all() instead of message_set.all() because we gave a related_name in the Message model
    # here we can see the importance of naming the model attribute, 
    # if we had not given a related_name, profile.message_set.all() does not know whether to use the sender or recipient
    
    unreadCount = messageRequests.filter(is_read=False).count()
    
    context = {
        'messageRequests': messageRequests,
        'unreadCount': unreadCount
    }
    
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    # make sure to not name the variable as "messages" because that name is used by our flash messages import
    message = profile.messages.get(id=pk)

    if message.is_read == False:
        # now make the message as read and save the message object
        message.is_read = True
        message.save()

        # to extend the read/unread functionality, we can add one more field to the model 
        # such as date_read to store when the message was first read

    context = {
        'message': message
    }
    return render(request, 'users/message.html', context)


# we want any user (logged in or not) to be able to send a message to another user
# so we are not adding the login_required decorator to this view
def createMessage(request, pk):
    # in this case the pk is used to get the recipient ID
    # recipient is used in the template to send the user back to the recipient profile when they hit the back button
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    sender = request.user.profile if request.user.is_authenticated else None 

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.recipient = recipient
            message.sender = sender

            # if sender profile exists, then set the message models' name and email fields from the sender profile
            if sender:
                message.name = sender.name
                message.email = sender.email
            
            message.save()

            messages.success(request, "Message sent successfully")

            return redirect('user-profile', pk=recipient.id)
            
    context = {
        'recipient': recipient,
        'form': form
    }
    return render(request, 'users/message_form.html', context)