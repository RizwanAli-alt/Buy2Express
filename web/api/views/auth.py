"""
Authentication API views.
POST /api/v1/auth/register/   – create account, returns JWT pair
POST /api/v1/auth/login/      – handled by SimpleJWT TokenObtainPairView
POST /api/v1/auth/logout/     – blacklist refresh token
GET/PUT /api/v1/auth/profile/ – view or update own profile
"""
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from ..serializers.auth import RegisterSerializer, ProfileSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    POST /api/v1/auth/register/

    Body: { username, email, password, password2, first_name, last_name }
    Returns: { user: {...}, tokens: { access, refresh } }
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': ProfileSerializer(user, context={'request': request}).data,
            'tokens': {
                'access':  str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    """
    POST /api/v1/auth/logout/

    Body: { refresh: "<token>" }
    Blacklists the refresh token so it can't be reused.
    Requires the `rest_framework_simplejwt.token_blacklist` app to be installed.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_205_RESET_CONTENT)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/v1/auth/profile/ – return current user's profile
    PUT  /api/v1/auth/profile/ – update profile (supports partial PATCH too)
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user