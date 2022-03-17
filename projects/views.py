from turtle import right
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
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
    # projects = Project.objects.all()
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()  # many to many relationship query

    context = {
        'project': projectObj,
        'tags': tags
    }
    return render(request, 'projects/single-project.html', context)


@login_required(login_url="login")
def createProject(request):
    # getting the current logged in user
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            # getting an instance of the form data but not yet saving it to db because we want to add the project owner
            project = form.save(commit=False)
            # use the current logged in user as the project owner
            project.owner = profile
            project.save()
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
        # by passing in the instance, we are telling Django which instance to update instead of adding a new record
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
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
