from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("settings/", views.settings, name="settings"),
    path("search/", views.search, name="search"),
    path("send/", views.send_message, name="send-message"),
    path("chat/<str:recipient>/", views.chat, name="chat"),
    path("profile/<str:username>/", views.profile, name="profile"),
]