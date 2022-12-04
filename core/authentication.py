from rest_framework.authentication import TokenAuthentication

class MyAuthentication(TokenAuthentication):
    keyword = 'Bearer'