from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, update_session_auth_hash
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import jwt
# from jwt import exceptions as jwtexceptions

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import (RegisterSerializer, SetLoginJWTSerializer, ChangePasswordSerializer, 
                        ResendActivationLinkSerializer, ResetPasswordLinkSerializer,
                        ResetPasswordSerializer)
from ...models import MyUser
from .utils import EmailThread

## Create Func Views here
@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['POST'])
def register_new_user_api(request):
    if request.method == "POST":
        ## create user account
        serializer = RegisterSerializer(data=request.data,  context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        ## create jwt refresh token
        user_email = serializer.validated_data['email']
        access_token = str(RefreshToken.for_user(user).access_token)
        # Context for your templates
        context = {
            'email': user_email,
            'site_name': 'To Do App',
            'activation_link': access_token,
        }
        # firstly, render the TEXT content.
        text_content = render_to_string("emails/activation_link.txt", context)
        # Secondly, render the HTML content.
        html_content = render_to_string("emails/activation_link.html", context)
        # Then, create a multipart email instance.
        msg = EmailMultiAlternatives(
            subject="Verifying Activation Link",
            body=text_content,
            from_email="ToDoApp-Func@example.com",
            to=[user_email],
            headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
        )
        # Lastly, attach the HTML content to the email instance and send.
        msg.attach_alternative(html_content, "text/html")
        EmailThread(email_obj=msg).start()
        messages = {
            'message': 'User Created Successfully',
            "detail": "activation link sent to your email."
        }
        return Response(messages, status=status.HTTP_200_OK)

@api_view()
def active_user_registeration_api(request, token):
    try:
        decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decode_token.get('user_id')
    except jwt.exceptions.ExpiredSignatureError:
        return Response({'details': 'token has been expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.InvalidSignatureError:
        return Response({'details': 'token is invalid'}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(MyUser, id=user_id)
    if user.is_active:
        return Response({'details': 'Your account is ALREADY activated!!!'})
    user.is_active = True
    user.save()
    return Response({'details': 'Your account is verified & activated'})

@swagger_auto_schema(
    method='post',
    request_body=ResendActivationLinkSerializer,
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['POST'])
def resend_activation_link_api(request):
    if request.method == 'POST':
        serializer = ResendActivationLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = get_object_or_404(MyUser, email=serializer.validated_data['email'])
        user = serializer.validated_data['user']  
        access_token = str(RefreshToken.for_user(user).access_token)
        # Context for your templates
        context = {
            'email': serializer.validated_data['email'],
            'site_name': 'To Do App',
            'activation_link': access_token,
        }
        # firstly, render the TEXT content.
        text_content = render_to_string("emails/activation_link.txt", context)
        # Secondly, render the HTML content.
        html_content = render_to_string("emails/activation_link.html", context)
        # Then, create a multipart email instance.
        msg = EmailMultiAlternatives(
            subject="Verifying Activation Link",
            body=text_content,
            from_email="ToDoApp-Func@example.com",
            to=[serializer.validated_data['email']],
            headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
        )
        # Lastly, attach the HTML content to the email instance and send.
        msg.attach_alternative(html_content, "text/html")
        EmailThread(email_obj=msg).start()
        return Response({"detail": "activation link resent to you."}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    request_body=ChangePasswordSerializer,
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_api(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    # CRITICAL: Updating the session hash prevents Django from logging the user out of their current session after changing their password.
    update_session_auth_hash(request, user)
    return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    request_body=ResetPasswordLinkSerializer,
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['POST'])
def reset_password_link_api(request):
    serializer = ResetPasswordLinkSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(MyUser, email=serializer.validated_data['email'])
    if not user:
        return Response({'detail': 'This user account doesn\'t exist!'})
    
    access_token = str(RefreshToken.for_user(user).access_token)
    context = {
            'email': user.email,
            'site_name': 'To Do App',
            'activation_link': access_token,
        }
    # firstly, render the TEXT content.
    text_content = render_to_string("emails/activation_link.txt", context)
    # Secondly, render the HTML content.
    html_content = render_to_string("emails/activation_link.html", context)
    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        subject="Reset Password",
        body=text_content,
        from_email="ToDoApp-Func@example.com",
        to=[user.email],
        headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
    )
    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    EmailThread(email_obj=msg).start()
    messages = {
        'message': 'Rest Password link sent to your mailbox'
    }
    return Response(messages, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    request_body=ResetPasswordSerializer,
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['POST'])
def reset_password_api(request, token):
    try:
        decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decode_token.get('user_id')
    except jwt.exceptions.ExpiredSignatureError:
        return Response({'details': 'token has been expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.InvalidSignatureError:
        return Response({'details': 'token is invalid'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ResetPasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(MyUser, id=user_id)
    user.set_password(serializer.validated_data['password'])
    user.save()
    return Response({'detail': 'New password has bees set correctly'})

@swagger_auto_schema(
    method='post',
    request_body=AuthTokenSerializer,
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['POST'])
def custom_login_auth_token(request):
    if request.method == 'POST':
        serializer = AuthTokenSerializer(data=request.data,  context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'email': user.email,
            'user_id': user.pk
        }
        return Response(data)

@swagger_auto_schema(
    method='post',
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_auth_token(request):
    try:
        # Delete the token associated with the requesting user
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."},
                        status=status.HTTP_204_NO_CONTENT)
    except AttributeError:
        # If the user doesn't have a token for some reason
        return Response({"detail": "No token found for this user."},
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@swagger_auto_schema(
    method='post',
    request_body=SetLoginJWTSerializer,
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['POST'])
def custom_login_jwt(request):
    """
    Authenticate user and return JWT tokens along with user details.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)

    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
    # Generate tokens for the authenticated user
    refresh = RefreshToken.for_user(user)
    # Return custom response with tokens and user data
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'email': user.email,
        'user_id': user.id,
        # Add any other user model fields you need
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def custom_logout_jwt(request):
    """
    Logout user by blacklisting their refresh token.
    """
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Attempt to blacklist the provided refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'success': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    except TokenError:
        # Token is invalid or has already been blacklisted
        return Response({'error': 'Invalid or expired refresh token'},
                        status=status.HTTP_400_BAD_REQUEST)  
    
