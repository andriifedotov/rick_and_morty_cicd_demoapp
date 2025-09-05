from django.urls import path
from .views import CharacterListView

urlpatterns = [
    path("characters/", CharacterListView.as_view(), name="characters-list"),
]