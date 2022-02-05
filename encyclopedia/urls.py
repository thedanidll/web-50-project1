from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name ="search"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("random", views.random, name="random")
]
