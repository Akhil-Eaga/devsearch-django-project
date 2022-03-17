from re import search
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .utils import paginateProfiles, searchProfiles
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm

# Create your views here.


def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

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
            return redirect("profiles")
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

        else:
            messages.error(request, "An error has occured during registration")

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
