from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

# Custom TokenObtainPairSerializer to include email and username in the response
class CustomClaimTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # custom claims
        token['username'] = user.username
        token['email'] = user.email
        
        return token
    