from django.urls import path
from .views import index,people,LoginAPI,PeopleAPI,RegisterApi,PeopleViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'person',PeopleViewset,basename='person')


urlpatterns = [
    path('index/', index),
    path('people/',people),
    path('Login/',LoginAPI.as_view()),
    path('peopleAPi/',PeopleAPI.as_view()),
    path('register/',RegisterApi.as_view()),    
]

urlpatterns += router.urls