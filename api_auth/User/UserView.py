from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.CustomPermissions.CustomPermissions import IsAdminOrManager
from core.UserManager.UserHandler import UserHandler


class UserLogin(APIView):
    """
    View responsible for loging in the user
    """

    def post(self, request):
        return UserHandler.handler_user_login(request_data=request.data)


class UserRegistration(APIView):
    """
    View responsible for registering the user
    """

    def post(self, request):
        return UserHandler.handler_user_registration(request_data=request.data)


class UserUpdate(APIView):
    """
    View responsible for updating user info
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        return UserHandler.handler_user_update(request.data, request.user)


class UserGetInfo(APIView):
    """
    View response for getting user information
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        return UserHandler.handler_get_user_info(request.user)


class ChangePassword(APIView):
    """
    View responsible for updating user password
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        return UserHandler.handler_user_change_password(request.data, request.user)


class MakeManager(APIView):
    permission_classes = (IsAuthenticated, IsAdminOrManager)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        return UserHandler.handler_make_user_manager(request.data)
