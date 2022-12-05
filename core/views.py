from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .authentication import MyAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from . models import User
from . serializers import UserRegistrationSerializer, UserSerializer, UpdateUserSerializer
from logging import *
import structlog

logger = structlog.get_logger(__name__)


def check_premium(paid, is_premium):
    """ returns tryue if the user paid Rs.100 and passed true to the field premium """
    if paid is True and is_premium is True:
        return True
    
    if paid is True and is_premium is False:
        raise ValidationError({'error': 'premium must be True is paid is True'})
    
    if paid is False and is_premium is True:
        raise ValidationError({'error': 'paid must be True is premium is True'})

    return False

# Create your views here.
@api_view(http_method_names=['post'])
@permission_classes([AllowAny])
def register_user(request):
    """ 
    Registers the user and returns the user credentials
    with their token.
    """
    if request.method == 'POST':
        data = request.data
        serializer = UserRegistrationSerializer(data=data)

        if serializer.is_valid(raise_exception=True):

            validated_data = serializer.validated_data

            user = User()
            user.username = validated_data['username']
            user.email = validated_data['email']
            user.phone = validated_data['phone']
            user.first_name = validated_data['first_name']
            user.last_name = validated_data['last_name']
            user.created_by = validated_data['username']
            user.modified_by = validated_data['username']
            user.set_password(validated_data['password'])
            user.premium = check_premium(paid=validated_data['paid'], is_premium=validated_data['premium'])
            user.save()
            Token.objects.create(user=user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['post'])
@permission_classes([AllowAny])
def login_user(request):
    """ 
    Login the user and returns the user credentials
    with their token.
    """
    if request.method == 'POST':
        data = request.data
        user = None

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise ValidationError({'error': 'user does not exist'})

        if not user.check_password(data['password']):
            return Response({'error': 'invalid password'})

        user_token, created = Token.objects.get_or_create(user=user)
        user_credentials = {
            'user': UserSerializer(user).data,
            'token': user_token.key
        }
        return Response(user_credentials, status=status.HTTP_202_ACCEPTED)


@api_view()
@permission_classes([AllowAny])
def user_list(request):
    """ Returns all the users """
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['get', 'put', 'delete'])
@authentication_classes([MyAuthentication])
def current_user(request: HttpRequest):
    """ 
    Returns the current user etails.
    This endpoint can be used to update or delete the current user
    """
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
            raise ValidationError({'error': 'user does not exist'})

    logger.info(f'USER --> {user}')
    
    if request.method == 'GET':
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        data = request.data
        serializer = UpdateUserSerializer(data=data)


        if serializer.is_valid(raise_exception=True):

            validated_data = serializer.validated_data

            user.username = validated_data['username']
            user.email = validated_data['email']
            user.phone = validated_data['phone']
            user.first_name = validated_data['first_name']
            user.last_name = validated_data['last_name']
            user.modified_by = validated_data['modified_by']
            user.premium = check_premium(paid=validated_data['paid'], is_premium=validated_data['premium'])
            user.save()

            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        Token.objects.get(user=user).delete()
        user.delete()
        return Response(f'deleted successfully', status=status.HTTP_204_NO_CONTENT)
