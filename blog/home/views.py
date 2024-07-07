from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BLogSerializer
from rest_framework import status
from rest_framework_simplejwt.authentication  import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Blog
from django.db.models import Q
from django.core.paginator import Paginator


class PublicBlog(APIView):
    def get(self,request):
        try:
            objs = Blog.objects.all().order_by("?")
            if request.GET.get('search'):
                search = request.GET.get('search')
                objs = objs.filter(Q(title__icontains=search)|Q(blog_text__icontains=search))
            
            page_number = request.GET.get('page',1)
            paginator = Paginator(objs,1)
            serializer = BLogSerializer(paginator.page(page_number),many = True)

            return Response({
                'data':serializer.data,
                'message':"Blog fetched successfully"
            },status=status.HTTP_200_OK)
        
        
        except Exception as e:
            return Response({'data':{},
                             "message":'something went wrong12'
                             },status=status.HTTP_400_BAD_REQUEST)


#  your views here.
class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication ]

    def get(self,request):
        try:
            objs = Blog.objects.filter(user = request.user)
            if request.GET.get('search'):
                search = request.GET.get('search')
                objs = objs.filter(Q(title__icontains=search)|Q(blog_text__icontains=search))
            serializer = BLogSerializer(objs,many = True)

            return Response({
                'data':serializer.data,
                'message':"Blog fetched successfully"
            },status=status.HTTP_200_OK)
        
        
        except Exception as e:
            return Response({'data':{},
                             "message":'something went wrong12'
                             },status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        try:
            data = request.data 
            data['user'] = request.user.id
            serializer = BLogSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'something went wrong'
                },status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                    'data':serializer.data,
                    'message':'blog created successfully',
                },status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'data':{},
                             "message":'something went wrong'
                             },status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request):
        try:
            data = request.data 
            blog = Blog.objects.filter(id = data.get('id'))
            print(blog[0])

            if not blog.exists():
                return Response({
                    'data':{},
                    'message':'Invalid blog id',
                },status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message':'You are not authorized to this',
                },status=status.HTTP_401_UNAUTHORIZED)
                


            serializer = BLogSerializer(blog[0],data=data,partial = True)
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'something went wrong'
                },status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                    'data':serializer.data,
                    'message':'blog updated successfully',
                },status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'data':{},
                             "message":'something went wrong'
                             },status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request):
        try:
            data = request.data 
            blog = Blog.objects.filter(id = data.get('id'))

            if not blog.exists():
                return Response({
                    'data':{},
                    'message':'Invalid blog id',
                },status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message':'You are not authorized to this',
                },status=status.HTTP_401_UNAUTHORIZED)
                

            blog[0].delete()

            return Response({
                    'data':{},
                    'message':'blog deleted successfully',
                },status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'data':{},
                             "message":'something went wrong'
                             },status=status.HTTP_400_BAD_REQUEST)
