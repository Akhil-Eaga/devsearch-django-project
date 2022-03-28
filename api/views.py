from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ProjectSerializer
from projects.models import Project

@api_view(['GET'])
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
    # if using the JsonResponse function, we will need the safe = False param in the return statement
    # but if we are using the rest frameworks' Response function, then the safe = False is not needed
    return Response(routes)


@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    # attempting to send the above projects list as a response will result in TypeError as the Project instance is not JSON serializable
    serializer = ProjectSerializer(projects, many=True) # many is set to True when we are serializer a list of Project instances
    
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)