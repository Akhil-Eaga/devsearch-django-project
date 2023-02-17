from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import paginateProjects, searchProjects


def projects(request):
    # searchProjects function is a helper function located in the projects/utils.py
    projects, search_query = searchProjects(request)
    results_per_page = 3

    custom_range, projects, paginator = paginateProjects(request, projects, results_per_page)
    
    context = {
        'projects': projects,
        'search_query': search_query,
        'paginator': paginator,
        'custom_range': custom_range,
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()  # many to many relationship query
    reviews = projectObj.review_set.all() # many to one relationship query
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        try:
            if form.is_valid():
                review = form.save(commit = False)
                # request.user.profile returns the currently logged in user
                review.owner = request.user.profile 
                review.project = projectObj
                review.save()

                # updating the vote counts and vote ratios
                projectObj.updateVoteCount
                # since we used the @property decorator on the updateVoteCount, 
                # we dont need to use the () as if it was a function call

                # notify the user that the review is submitted successfully
                messages.success(request, "Review submitted successfully")
                
                # to redirect to a url that takes in a dynamic value like the project id, this is the way to implement that
                # the reason for this redirection is to clear the form fields after submitting the review
                return redirect('project', pk=projectObj.id)

        except IntegrityError:
            messages.info(request, "You have already submitted a review or vote for this project")
            return redirect('project', pk=projectObj.id)

    context = {
        'project': projectObj,
        'tags': tags,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'projects/single-project.html', context)


@login_required(login_url="login")
def createProject(request):
    # getting the current logged in user
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # getting an instance of the form data but not yet saving it to db because we want to add the project owner
            project = form.save(commit=False)
            # use the current logged in user as the project owner
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            # the if condition is checking if the submitted form is valid or not
            # the form.save() actually saves the form data into the database
            # after saving, redirect the user to the projects page by calling that URL's alias or name
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    # by passing in the instance, we are initializing all the form fields
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        # by passing in the instance, we are telling Django which instance to update instead of adding a new record
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def deleteProject(request, pk):
    # getting the logged in user
    profile = request.user.profile
    # finding and setting the project variable to be deleted from only the projects that are owned by the logged in user
    project = profile.project_set.get(id=pk)

    if request.method == "POST":
        project.delete()
        return redirect('account')

    context = {'object': project}
    return render(request, 'delete_template.html', context)
