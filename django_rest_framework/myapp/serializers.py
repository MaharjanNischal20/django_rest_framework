from rest_framework import serializers
from .models import People,Color
from django.contrib.auth.models import User

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField() 
    email = serializers.EmailField()
    password = serializers.CharField() 

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'],email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    
    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("Username already exists")

        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError("Email already exists")       

        return data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class PeopleSerializer(serializers.ModelSerializer):
    # color = ColorSerializer()
    # color_info = serializers.SerializerMethodField()
    
    class Meta:
        model = People
        fields = '__all__'

    # def get_color_info(self,obj):
    #     color_obj = Color.objects.get(id = obj.color.id)
    #     return {'color_name':color_obj.color_name,'hex_code':'#000'}

    def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError("Age must be greate than 18")
        
        return data