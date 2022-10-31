from datetime import timedelta

from django.core.exceptions import BadRequest
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import (
    get_access_token_model,
    get_application_model,
    get_refresh_token_model,
)
from oauth2_provider.settings import oauth2_settings
from oauthlib import common
from social_django.utils import psa

EXPIRE_SECONDS = oauth2_settings.defaults["ACCESS_TOKEN_EXPIRE_SECONDS"]
Application = get_application_model()
AccessToken = get_access_token_model()
RefreshToken = get_refresh_token_model()


def create_access_token(user, client_id: str):
    application = Application.objects.get(
        client_id=client_id,
        client_type=Application.CLIENT_PUBLIC,
    )
    access_token = AccessToken.objects.create(
        user=user,
        expires=timezone.now() + timedelta(seconds=EXPIRE_SECONDS),
        token=common.generate_token(),
        application=application,
    )
    refresh_token = RefreshToken.objects.create(
        user=user,
        token=common.generate_token(),
        application=application,
        access_token=access_token,
    )

    return JsonResponse(
        {
            "access_token": access_token.token,
            "expires_in": EXPIRE_SECONDS,
            "token_type": "Bearer",
            "refresh_token": refresh_token.token,
        }
    )


@csrf_exempt
@psa()
def social_auth_token_exchange_view(request, backend, *args, **kwargs):
    try:
        if client_id := request.POST.get("client_id"):
            if token := request.POST.get("token"):
                user = request.backend.do_auth(token)
            else:
                if getattr(request.backend, "STATE_PARAMETER", False):  # pragma: no cover
                    request.backend.STATE_PARAMETER = False

                user = request.backend.complete()
            return create_access_token(user, client_id)
        raise BadRequest("Please provide client_id")
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)
