from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import AuthorizationView

app_name = "social_oauth_token"

urlpatterns = [
    path("token/<str:backend>/", csrf_exempt(AuthorizationView.as_view()), name="token"),
]
