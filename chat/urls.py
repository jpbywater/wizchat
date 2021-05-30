from django.urls import include, path

from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.index, name='index'),
    path('chat/start', views.start, name='start'),
    path('chat/interface', views.interface, name='interface'),
    path('chat/ozstart', views.ozstart, name='ozstart'),
    path('chat/ozinterface', views.ozinterface, name='ozinterface'),
]