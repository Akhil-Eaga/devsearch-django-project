# this file contains code and functions that are either meant to be helper functions
# or for the purpose of decluttering the code in the main files like the views.py


from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag



def paginateProjects(request, projects, results_per_page):
    page = request.GET.get('page')
    
    paginator = Paginator(projects, results_per_page)


    # from here the variable projects is not an array but rather of type page object
    # page object provides many methods and attributes, like the projects.number (returns current page),
    # projects.page_range returns a range object and 
    # projects.has_previous returns a boolean if a previous page exists or not
    # projects.previous_page_number returns the page number of the previous page
    # similarly projects.has_next returns a boolean if a next page exists or not
    # similarly projects.next_page_number returns the page number of the next page
    # projects.has_other_pages returns a boolean if pages other than the current one exists
    # all of these are methods (i.e., when accessed in code, they should have parentheses), 
    # but in jinja templates we access them without the parentheses
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # this code runs when the user first loads the webpage and there is no page
        # when the projects page is first loaded there are no query params (like /projects/?page=12)
        # so we simply show the first page to the user
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        # this code runs when the user tries to load a page thats out of the page range
        # for example, when user tries to load a 100th page while there are only 20 pages, we show the 20th page
        page = paginator.num_pages
        projects = paginator.page(page)

    # although pagination provided by django is good, but it falls apart when we have 1000 pages.
    # we do not want to display page numbers for all the pages
    # so we are about to create our own custom page range

    left_index = int(page) - 4
    left_index = left_index if left_index >= 1 else 1

    right_index = int(page) + 5
    right_index = right_index if right_index <= paginator.num_pages else paginator.num_pages

    custom_range = range(left_index, right_index + 1) # + 1 because upper extreme of the range is not inclusive
 
    # custom_range = range(1, 1000)
    return custom_range, projects, paginator


def searchProjects(request):
    # variable to hold the search query term
    search_query = ''

    # the 'search_query' string inside the request.GET.get is actually searching for the name of the
    # input field that is making this request. If you used a different name for the input field, then use that term
    # to search within the request. This is similar to how we got the next value to use in backlinks.
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    # to show projects that contains a tags that contains the search_query
    # here tags is not a child of the Project rather Project to Tag is a Many to Many relationship
    tags = Tag.objects.filter(name__icontains=search_query)

    # here we are trying to filter out the profiles based on names and WIHTOUT case sensitiveness
    # sometimes, chaining the conditions can have overlapping results, leading to duplicates
    # to avoid that we can chain in the distinct condition before using the filter
    projects = Project.objects.distinct().filter( 
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) | 
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags))

    # in the above search coditions, owner is a parent object referenced by the Project,
    # so to access the name of the owner object, we use owner__name (note the double underscore)
    return projects, search_query