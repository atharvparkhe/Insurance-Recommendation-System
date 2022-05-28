from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('signup/', views.signUp, name="signup"),
	path('login/', views.logIn, name="login"),
	path('forgot/', views.forgot, name="forgot"),
	path('reset/', views.reset, name="reset"),
	path('health/', views.health, name="health"),
	path('upload-data/', views.getData, name="upload-data"),
	path('check-data/', views.checkData, name="check-data"),
	path('analyse-data/', views.analyseData, name="analyse-data"),
	path('fetch-results/', views.fetchResults, name="fetch-results"),
]