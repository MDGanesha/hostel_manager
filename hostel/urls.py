from django.urls import path
from . import views
app_name = 'hostel'
urlpatterns = [
    path('',views.index,name='index')
]