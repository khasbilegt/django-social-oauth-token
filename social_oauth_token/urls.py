from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import AuthCodeTokenExchangeView

app_name = "social_oauth_token"

urlpatterns = [
    path("token/<str:backend>/", csrf_exempt(AuthCodeTokenExchangeView.as_view()), name="token"),
]
