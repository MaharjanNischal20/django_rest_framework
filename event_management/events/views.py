from rest_framework.response import Response
from .serializers import EventSerializer
from rest_framework.views import APIView
from .models import Event
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
from pathlib import Path
from rest_framework.permissions import IsAuthenticated


class JSONStorage:

    def __init__(self, file_path='events.json'):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            self.file_path.write_text(json.dumps([]))

    def read_data(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def write_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def get_all_events(self):
        return self.read_data()

    def add_event(self, event_data):
        events = self.read_data()
        events.append(event_data)
        self.write_data(events)

    def update_event(self, event_id, event_data):
        events = self.read_data()
        for index, event in enumerate(events):
            if event['id'] == event_id:
                events[index] = event_data
                break
        self.write_data(events)

    def delete_event(self, event_id):
        events = self.read_data()
        events = [event for event in events if event['id'] != event_id]
        self.write_data(events)


class EventListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        events = Event.objects.all()

        # Filtering
        title = request.query_params.get('title')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if title:
            events = events.filter(title__icontains=title)
        if start_date:
            events = events.filter(start_date__gte=start_date)
        if end_date:
            events = events.filter(end_date__lte=end_date)

        serializer = EventSerializer(events, many=True)
        return Response({
            'data': serializer.data,
            'message': "Fetched successfully"
        }, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data
            serializer = EventSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    "data": serializer.errors,
                    'message': 'Something went wrong',
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "data": serializer.data,
                'message': 'Event created successfully',
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "data": {},
                'message': f'Something went wrong: {str(e)}',
            }, status=status.HTTP_400_BAD_REQUEST)

class EventDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response({
            'data': serializer.data,
            'message': "Fetched successfully"
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            data = request.data
            event = get_object_or_404(Event, pk=pk)
            serializer = EventSerializer(event, data=data)
            if not serializer.is_valid():
                return Response({
                    "data": serializer.errors,
                    'message': 'Something went wrong',
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "data": serializer.data,
                'message': 'Event updated successfully',
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {},
                'message': f'Something went wrong: {str(e)}',
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            event = get_object_or_404(Event, pk=pk)
            event.delete()
            return Response({
                'data': {},
                'message': 'Event deleted successfully',
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'data': {},
                'message': f'Something went wrong: {str(e)}',
            }, status=status.HTTP_400_BAD_REQUEST)
