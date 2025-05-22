from django.urls import path
from .views import watchlist_view

urlpatterns = [
    path("watchlist/", watchlist_view, name="watchlist"),
]