from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("reload/", views.reload, name="reload"),
    path("authorization/", views.requestSpotifyAuthorization, name='requestSpotifyAuthorization'),
    path("token/", views.handleSpotifyCallback, name='handleSpotifyCallback'),
    path("playback/", views.interfacePlaybackControl, name="interfacePlaybackControl"),
    path('start/', views.startPersonalAssistant, name='startPersonalAssistant'),
    path('update/', views.updateOnInterface, name="updateOnInterface")
]