from datetime import timedelta

from django.contrib.auth import login
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import View
from oauth2_provider.models import (
    get_access_token_model,
    get_application_model,
    get_refresh_token_model,
)
from oauth2_provider.settings import oauth2_settings
from oauthlib import common
from social_core.exceptions import AuthCanceled, MissingBackend
from social_django.utils import load_backend, load_strategy

Application = get_application_model()


class AuthorizationView(View):
    def post(self, request, backend, *args, **kwargs):
        try:
            client_id = request.POST.get("client_id", None)
            user = self.get_user(request, backend)

            if backend and request.POST.get("code", None) and client_id and user:
                login(request, user)
                request.session.set_expiry(0)  # expire when the Web browser is closed
                return self.create_access_token(user, client_id)
        except MissingBackend:
            pass
        return JsonResponse({"message": "Bad Request"}, status=400)

    def get_user(self, request, backend_name: str):
        try:
            backend = load_backend(load_strategy(request), backend_name, None)

            # Backend -c шалтгаалан authorizationCode -г баталгаажуулах процесс
            # нь redirect хийхгүй учир state -г ашиглах шаардлагагүй

            if getattr(backend, "STATE_PARAMETER", False):  # pragma: no cover
                backend.STATE_PARAMETER = False

            return backend.complete()
        except AuthCanceled:
            return None

    def create_access_token(self, user, client_id: str):
        try:
            application = Application.objects.get(
                client_id=client_id,
                client_type=Application.CLIENT_PUBLIC,
            )
            access_token = get_access_token_model().objects.create(
                user=user,
                expires=timezone.now() + timedelta(seconds=oauth2_settings.defaults["ACCESS_TOKEN_EXPIRE_SECONDS"]),
                token=common.generate_token(),
                application=application,
            )
            refresh_token = get_refresh_token_model().objects.create(
                user=user,
                token=common.generate_token(),
                application=application,
                access_token=access_token,
            )

            return JsonResponse(
                {
                    "access_token": access_token.token,
                    "expires_in": access_token.expires,
                    "token_type": "Bearer",
                    "refresh_token": refresh_token.token,
                }
            )
        except Application.DoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=403)
