from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from .serializers import PeopleSerializer,LoginSerializer,RegisterSerializer
from .models import People
from rest_framework import viewsets,status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action


@api_view(['GET'])
def index(request):
    courses = {
        'course_name ' : 'python',
        'learn' : ['flask0','django','FastApi','Tornado'],
        'course_Provider': 'Nischal',
    }
    return Response(courses)


class LoginAPI(APIView):
    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status':False,
                "Message":serializer.errors},status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username = serializer.data['username'],password = serializer.data['password'])
        if not user:
            return Response({
                'status':False,
                "Message":"Invalid Credentials",},status.HTTP_400_BAD_REQUEST)
        token , _ = Token.objects.get_or_create(user=user)
        return Response({
            'status':True,
            'message':'Login Successful',  
            "token":str(token)   
        },status.HTTP_200_OK)



class PeopleAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        try:
            obj = People.objects.all()
            page = request.GET.get('page',1)
            page_size = 3
            paginator = Paginator(obj,page_size)
            serializer = PeopleSerializer(paginator.page(page),many = True)
            return Response(serializer.data)    
        except Exception as e:
            return Response({
                'status':False,
                'message':'invalid page',
            })
    
    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.errors)
    
    def patch(Self, request):
        data = request.data 
        objs = People.objects.get(id = data['id'])
        serializer = PeopleSerializer(objs, data=data,partial = True)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.errors)
    
    def put(Self, request):
        data = request.data 
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.errors)
    
    def delete(self,request):
        data = request.data 
        obj = People.objects.get(id = data['id'])
        obj.delete()
        return Response({"message":"deleted"})





@api_view(['GET','POST','PUT','PATCH','DELETE'])
def people(request):
    if request.method == 'GET':
        objs = People.objects.filter(color__isnull = False)
        serializer = PeopleSerializer(objs,many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method == 'PUT':
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method == 'PATCH':
        data = request.data
        objs = People.objects.get(id = data['id'])
        serializer = PeopleSerializer(objs,data=data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
            
    else:
        data = request.data
        objs = People.objects.get(id = data['id'])
        objs.delete()
        return Response({"Message":"Deleted"})
    

class PeopleViewset(viewsets.ModelViewSet):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer
    
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)
        serializer = PeopleSerializer(queryset,many = True)
        return Response({"data":serializer.data})
   
    @action(detail=True,methods=['POST'])
    def send_email(self,request,pk):
        print(pk)
        obj = People.objects.get(pk = pk)
        serializer = PeopleSerializer(obj)
        return Response({
            'status':True,
            'Message':"Email sent successfully",
            'data':serializer.data
        })


class RegisterApi(APIView):
    def post(self,request):
        data = request.data 
        serializer = RegisterSerializer(data= data)

        if not serializer.is_valid():
            return Response({
                'status':False,
                'message':serializer.errors,
                },status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return  Response({
            'status':True,
            'message':'User Created'
        },status.HTTP_201_CREATED)
    
