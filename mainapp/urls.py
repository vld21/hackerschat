from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('createroom/', views.CreateRoom.as_view(), name='create_room'),
    path('topics/<str:topic_name>/', views.ChatView.as_view(), name='chat_room'),
    path('topics/<str:topic_name>/chat/archive/', views.ChatArchive.as_view(), name='chat_archive'),
    path('roomslist/', views.RoomsList.as_view(), name='rooms_list'),
    path('search/', views.SearchView.as_view(), name='search_view'),
    path('chatsubscription/', views.ChatRoomSubscription.as_view(), name='chat_subscription'),
]