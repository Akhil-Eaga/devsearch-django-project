from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('projects/', views.getProjects, name="projects"),
    path('projects/<str:pk>/', views.getProject, name="project"),
]

# Although it makes more sense to use the route as project/<str:pk>, but to keep the API more
# Restful, we are going to use the "projects/<str:pk>" instead of "project/<str:pk>" as the route