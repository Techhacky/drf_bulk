from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer

class BulkUpdateCreateView(APIView):

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request):
        data = request.data

        # Loop through the data and perform updates
        for item in data:
            instance_id = item.get('id')
            if instance_id is not None:
               
                    instance = Task.objects.get(id=instance_id)
                    serializer =TaskSerializer(instance, data=item, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
               

        return Response("Bulk update successful.", status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        # Create objects in a loop
        serialized_data = []
        for item in data:
            serializer =TaskSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
                serialized_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serialized_data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        data = request.data

       
        if not data or not isinstance(data, list) or len(data) == 0:
            return Response("Request body is empty or contains an empty list.", status=status.HTTP_400_BAD_REQUEST)

      
        instance_ids = [item.get('id') for item in data if item.get('id') is not None]

       
        existing_instances = Task.objects.filter(id__in=instance_ids)

      
        existing_instances_dict = {instance.id: instance for instance in existing_instances}

        
        for instance_id in instance_ids:
            instance = existing_instances_dict.get(instance_id)
            if instance:
                instance.delete()
            else:
                return Response(f"Object with id {instance_id} does not exist.", status=status.HTTP_404_NOT_FOUND)

        return Response("Bulk delete successful.", status=status.HTTP_204_NO_CONTENT)
