from django.urls import path
from .views import *


urlpatterns = [
	path('<str:hash>/', FileStorage.as_view()),
	path('', FileStorage.as_view()),
]