from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('projects/', views.getProjects, name="api-projects"), # the name is prefixed with "api-" to prevent name clash with the normal 'projects' route
    path('projects/<str:pk>/', views.getProject, name="api-project"), # the name is prefixed with "api-" to prevent name with the normal 'project' routes
    path('projects/<str:pk>/vote/', views.projectVote, name="vote"),
]

# Although it makes more sense to use the route as project/<str:pk>, but to keep the API more
# Restful, we are going to use the "projects/<str:pk>" instead of "project/<str:pk>" as the route