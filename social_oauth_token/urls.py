from django.urls import path

from .views import social_auth_token_exchange_view

app_name = "social_oauth_token"

urlpatterns = [
    path("token/<str:backend>/", social_auth_token_exchange_view, name="token"),
]
