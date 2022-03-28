from django.http import JsonResponse


def getRoutes(request):

    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

        {'POST': '/api/users/token'}, # this one is provided by django as a CBV, tokens have an expiration date
        {'POST': '/api/users/token/refresh'} # this one is used to stay logged in by accessing the refreshed token

    ]

    # the safe parameter tells JsonResponse that we can return back somethingo other than a python dictionary
    # adding this parameter enables us to turn any data into json data
    return JsonResponse(routes, safe=False)