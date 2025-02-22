from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User


class RegisterView(APIView):
    def get(self,request):
        objs = User.objects.all()
        serializer = RegisterSerializer(objs,many= True)
        return Response(serializer.data)


    def post(self, request):
        try:
            data = request.data 
            serializer = RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    "data":serializer.errors,
                    "message":"Something went wrong",
                },status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data':serializer.data,
                'message':'Registration Successful',
            },status=status.HTTP_201_CREATED)

        except Exception as e: 
            return Response({
                    "message":"Something went wrong",
                },status=status.HTTP_400_BAD_REQUEST)  

class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data 
            serializer = LoginSerializer(data=data)
            if not serializer.is_valid():
                    return Response({
                        "data":serializer.errors,
                        "message":"Something went wrong",
                    },status=status.HTTP_400_BAD_REQUEST)  
            response = serializer.get_jwt_token(serializer.data)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e: 
            return Response({
                'data':{},
                    "message":"Something went wrong",
                },status=status.HTTP_400_BAD_REQUEST)

