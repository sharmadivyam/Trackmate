from rest_framework import serializers
from .models import User, Task
from django.contrib.auth.hashers import check_password


from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer (serializers.ModelSerializer):
        password1 = serializers.CharField(write_only=True, required =False)
        password2 = serializers.CharField(write_only=True, required =False)
        username = serializers.CharField(write_only=True, required =False)
        email = serializers.EmailField(write_only=True, required=True)
        password = serializers.CharField(write_only=True, required=False)
        reporting_manager = serializers.CharField(write_only= True, required = False)
        name = serializers.CharField(write_only= True, required = False)
        class Meta:
            model = User
            fields = ['username','email','name','password1','password2','password','reporting_manager']

    
        def validate(self,data):
            mode = self.context.get("mode")
            if mode == "signup":
                if data['password1'] != data['password2']:
                    raise serializers.ValidationError("passwords do not match , try again")
                if User.objects.filter(email=data['email']).exists()==True :
                    raise serializers.ValidationError("Email id already registered")
                return data
            elif mode == "login":
                try:
                    user = User.objects.get(email=data['email'])
                except User.DoesNotExist:
                    raise serializers.ValidationError("Email ID not registered.")

                if not check_password(data['password'], user.password):
                    raise serializers.ValidationError("Incorrect password.")
 
                data['user'] = user
                return data

            raise serializers.ValidationError("Invalid mode.")
        def create(self, validated_data):

            user = User.objects.create_user(
                username=validated_data["email"],
                email=validated_data["email"],
                first_name=validated_data["name"],
                password=validated_data["password1"],
                reporting_manager = validated_data["reporting_manager"],
            )
            user.save()
            print("user saved succesfully",user)
            return user 


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task', 'details', 'start_date', 'deadline', 'progress', 'last_update', 'category']

    def create(self,validated_data):
        user = self.context['request'].user
        task = Task.objects.create(
            userid = user, **validated_data   #used ** to unpack the dictionary
        )
        task.save()
        return task