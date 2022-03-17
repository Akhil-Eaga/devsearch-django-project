# this file contains all the helper functions that are used within the users app and 
# this file contains the function that are either reusable or to keep the code organized within views.

from .models import Skill, Profile
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results_per_page):
    page = request.GET.get('page')
    
    paginator = Paginator(profiles, results_per_page)


    # from here the variable profiles is not an array but rather of type page object
    # page object provides many methods and attributes, like the profiles.number (returns current page),
    # profiles.page_range returns a range object and 
    # profiles.has_previous returns a boolean if a previous page exists or not
    # profiles.previous_page_number returns the page number of the previous page
    # similarly profiles.has_next returns a boolean if a next page exists or not
    # similarly profiles.next_page_number returns the page number of the next page
    # profiles.has_other_pages returns a boolean if pages other than the current one exists
    # all of these are methods (i.e., when accessed in code, they should have parentheses), 
    # but in jinja templates we access them without the parentheses
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        # this code runs when the user first loads the webpage and there is no page
        # when the profiles page is first loaded there are no query params (like /profiles/?page=12)
        # so we simply show the first page to the user
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        # this code runs when the user tries to load a page thats out of the page range
        # for example, when user tries to load a 100th page while there are only 20 pages, we show the 20th page
        page = paginator.num_pages
        profiles = paginator.page(page)

    # although pagination provided by django is good, but it falls apart when we have 1000 pages.
    # we do not want to display page numbers for all the pages
    # so we are about to create our own custom page range

    left_index = int(page) - 4
    left_index = left_index if left_index >= 1 else 1

    right_index = int(page) + 5
    right_index = right_index if right_index <= paginator.num_pages else paginator.num_pages

    custom_range = range(left_index, right_index + 1) # + 1 because upper extreme of the range is not inclusive
 
    # custom_range = range(1, 1000)
    return custom_range, profiles, paginator    


def searchProfiles(request):
    # variable to hold the search query term
    search_query = ''

    # the 'search_query' string inside the request.GET.get is actually searching for the name of the
    # input field that is making this request. If you used a different name for the input field, then use that term
    # to search within the request. This is similar to how we got the next value to use in backlinks.
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    # to show profiles that contains a skill that contains the search_query
    # here in this case skills is a child object (i.e., Profile to Skill is a One to Many relation)
    skills = Skill.objects.filter(name__icontains=search_query)

    # here we are trying to filter out the profiles based on names and WIHTOUT case sensitiveness
    # sometimes, chaining the conditions can have overlapping results, leading to duplicates
    # to avoid that we can chain in the distinct condition before using the filter
    profiles = Profile.objects.distinct().filter( 
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) | 
        Q(skill__in=skills) )

    return profiles, search_query