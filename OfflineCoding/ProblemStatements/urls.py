from django.urls import path
from . import views
app_name='ProblemStatements'

urlpatterns = [
    path('',views.home,name='home'),
    path('download/',views.download,name='download'),
]
