from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import CustomerSerializer, TransactionSerializer, UserSerializer, UserSerializerWithToken
from .models import Customer, Transaction
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.db.models import Q


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        try:
            if User.objects.filter(Q(username=data['username']) | Q(email=data['email'])).exists():
                return Response({'detail': 'User with this username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                password=make_password(data['password']),
            )
            user.is_staff = data.get('is_staff', False)
            user.is_superuser = data.get('is_superuser', False)
            user.save()
            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'detail': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)


class CustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id  # Set the current user as the customer creator
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Success'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors, 'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Success'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors, 'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
