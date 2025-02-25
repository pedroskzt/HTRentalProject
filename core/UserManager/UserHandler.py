from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_auth.User.UserModel import User
from api_auth.User.serializers import (UserSerializer, UserUpdateSerializer, UserInfoSerializer)
from core.CustomErrors.CustomErrors import CustomError
from core.UserManager.UserHelper import UserHelper


class UserHandler:
    @staticmethod
    def handler_user_login(request_data):
        """
        Handler for login in the user.
        References: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/creating_tokens_manually.html
        https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#authentication-backends
        :param request_data: Username and password in JSON format.
        :return: JSON response with HTTP status code.
        """
        try:
            email = request_data.get('username')
            password = request_data.get('password')
            if email and password:
                try:
                    user = UserHelper.get_user_by_email(email)
                except User.DoesNotExist as e:
                    return Response(CustomError.get_error_by_code("UE-0", e), status=status.HTTP_400_BAD_REQUEST)

                if user.check_password(password):
                    # The user exists and the password is correct then create a Token and return it.
                    token = RefreshToken.for_user(user)
                    response_data = {'refresh': str(token),
                                     'access': str(token.access_token)}
                    return Response(response_data, status=status.HTTP_200_OK)
            return Response(CustomError.get_error_by_code("UE-0"), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_user_registration(request_data):
        """
        Handler for register a new user.
        :param request_data:{
                            "first_name": "John",
                            "last_name": "Manager",
                            "email": "j.manager@example.com",
                            "password": "Password@123",
                            "address": "123 JhonDoe Street",
                            "phone_number": "+1 98765432"
                        }
        :return:
        """
        try:
            request_data['username'] = request_data.get('email')
            user_serializer = UserSerializer(data=request_data)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(CustomError.get_error_by_code("GE-0", user_serializer.errors),
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_user_update(request_data, user):
        """
        Handler for updating user information. It validates the passed values and updated only the passed fields.
        Updatable fields:
        - first_name
        - last_name
        - address
        - phone_number

        :param request_data:
        :param user:
        :return:
        """
        try:
            user_serializer = UserUpdateSerializer(user, data=request_data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_202_ACCEPTED)

            return Response(CustomError.get_error_by_code("GE-0", user_serializer.errors),
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_get_user_info(user):
        """
        Handler for getting user info.

        :param user:
        :return: dict with user info - first name, last name, email,address, phone number
        """
        try:
            serialized_user = UserInfoSerializer(user)

            if serialized_user:
                return Response(serialized_user.data, status=status.HTTP_200_OK)

            return Response(CustomError.get_error_by_code("UE-2"), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_user_change_password(request_data, user):
        """
        Handler for changing user password.
        Password requirements:
        Must have at least 8 characters
        Must contain at least 1 number
        Must contain at least 1 letter
        Must contain at least 1 special character
        Cannot match one of the user attributes (first_name, last_name, email)
        :param user:
        :param request_data:
        :return: success message
        """
        try:
            if "password" not in request_data or request_data.get('password') is None:
                return Response(CustomError.get_error_by_code("UE-3"),
                                status=status.HTTP_400_BAD_REQUEST)

            # If any of the validations fail, an exception will be raised
            validate_password(request_data.get('password'))
            user.set_password(request_data.get('password'))
            user.save()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_make_user_manager(request_data):
        try:
            user = UserHelper.get_user_by_email(request_data.get('email'))
            manager_group = UserHelper.get_manager_group()
            if manager_group.exists() is False:
                return Response(CustomError.get_error_by_code("UE-4"), status=status.HTTP_400_BAD_REQUEST)
            manager_group = manager_group.first()

            if manager_group in user.groups.all():
                return Response(CustomError.get_error_by_code("UE-5"), status=status.HTTP_400_BAD_REQUEST)

            user.groups.add(manager_group)

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status=status.HTTP_400_BAD_REQUEST)
