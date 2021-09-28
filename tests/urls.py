from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import include, path
from django.views.generic import TemplateView


class ProfileView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return HttpResponse()


urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("", include("social_oauth_token.urls", namespace="social_oauth_token")),
]
