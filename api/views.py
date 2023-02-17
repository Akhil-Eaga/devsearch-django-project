from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .serializers import ProjectSerializer
from projects.models import Project, Review

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
# @permission_classes([IsAuthenticated]) # this is analogous to the @login_required decorator for our normal jinja views
def getProjects(request):
    # this "request.user" does not look for user based on session based login, 
    # but the @api_view decorator ensures that the request.user is actually looking for JWT based authenticated user
    # print("USER:", request.user)
    projects = Project.objects.all()
    # attempting to send the above projects list as a response will result in TypeError as the Project instance is not JSON serializable
    serializer = ProjectSerializer(projects, many=True) # many is set to True when we are serializer a list of Project instances
    
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    # note that user comes from the token in this case not the Django's default session based login
    user = request.user.profile

    # request.data is not generally available on the request object, but because of the api_view decorator it is available
    data = request.data

    # get_or_create will check if a review by the current user on the current project already exists and returns that object
    # if there is not such match, it creates a new review for the user on the given project and makes the "created" boolean a true else false
    review, created = Review.objects.get_or_create(
        owner=user,
        project=project
    )
    # updating the vote value using the data object received from the 
    review.value = data['value']
    review.save()
    # calling the update vote count to update the vote count and the vote ratio
    project.updateVoteCount

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)