from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django .http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken



@csrf_exempt
@api_view(['POST'])
def register_user(request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User created"}, status=201)

@csrf_exempt
@api_view(['POST'])
def login_user(request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=200)
        
        return JsonResponse({"error": "Invalid credentials"}, status=400)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')

        task = Task.objects.create(user=request.user, title=title, description=description)
        return JsonResponse({'message': 'Task created successfully', 'task_id': task.id})
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tasks(request):
        tasks = Task.objects.filter(user=request.user).values('id', 'title', 'description', 'completed')
        return JsonResponse(list(tasks), safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task(request, task_id):
    """
    Retrieves a specific task by ID.
    """
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        return JsonResponse({
            "task": task.title,
            "description": task.description,
            "completed": task.completed,
        })
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.title = data.get("title", task.title)
            task.description = data.get("description", task.description)
            task.completed = data.get('completed', task.completed)
            task.save()

            return JsonResponse({"message": "Task updated"})
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
        
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    if request.method == 'DELETE':
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.delete()
            return JsonResponse({"message": "Task deleted"})
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)

@api_view(['POST'])        
def user_logout(request):
    return JsonResponse({"message": "Logout successful"})