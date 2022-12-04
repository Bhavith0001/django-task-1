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
from . serializers import UserRegistrationSerializer, UserSerializer

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
            user = User()
            user.username = data['username']
            user.email = data['email']
            user.phone = data['phone']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.created_by = data['username']
            user.modified_by = data['username']
            user.set_password(data['password'])
            user.save()
            Token.objects.create(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


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
def me(request: HttpRequest):
    """ 
    Returns the current user etails.
    This endpoint can be used to update or delete the current user
    """
    user = User.objects.get(id=request.user.id)

    if request.method == 'GET':
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        data = request.data
        
        user.username = data['username']
        user.email = data['email']
        user.phone = data['phone']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.modified_by = data['modified_by']
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        Token.objects.get(user=user).delete()
        user.delete()
        return Response(f'deleted successfully', status=status.HTTP_204_NO_CONTENT)

