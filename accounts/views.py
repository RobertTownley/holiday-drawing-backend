from drawings.serializers import ParticipantSerializer
from django.conf import settings
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer


@api_view(["POST"])
def login_view(request):
    try:
        user = User.objects.get(username=request.data.get("username"))
    except User.DoesNotExist:
        return Response(
            {"msg": "Could not login with that username and password"}, status=400
        )
    if not user.check_password(request.data.get("password")):
        return Response(
            {"msg": "Could not login with that username and password"}, status=400
        )
    token, created = Token.objects.get_or_create(user=user)
    return Response(
        {
            "token": token.key,
        }
    )


@api_view(["POST"])
def registration_view(request):
    username = request.data.get("username", "").lower()
    password = request.data.get("password")
    family_code = request.data.get("familyCode")
    if family_code != settings.FAMILY_CODE:
        return Response({"msg": "Family code was incorrect"}, status=400)
    user_exists = User.objects.filter(username=username).exists()
    if user_exists:
        return Response(
            {
                "msg": "User with that email already exists",
            },
            status=400,
        )
    if not username or not password:
        return Response(
            {"msg": "Username and password required"},
            status=400,
        )
    if User.objects.filter(username=username).exists():
        return Response(
            {"msg": "Username already in use"},
            status=400,
        )

    user = User.objects.create_user(
        username=username, email=username, password=password
    )
    token, created = Token.objects.get_or_create(user=user)
    return Response(
        {
            "token": token.key,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_view(request):
    return Response(
        {
            "id": request.user.id,
        }
    )
