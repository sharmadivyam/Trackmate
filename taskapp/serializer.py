from rest_framework import serializers
from .models import User

class UserSerializer (serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email','password1','password2','name']

    def validate_email(self,value):
        if User.objects.filter(email=value).exists()==True :
            raise serializers.ValidationError("Email id already registered")
        return value
    
    def validate(self,data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("passwords do not match , try again")
        return data
    
    def create(self,validated_data):
        user = User.objects.create_user( 
            username = validated_data['email'],
            email= validated_data["email"],
            first_name= validated_data["name"],
            password = validated_data["password1"]
        )
        user.save()
        return user