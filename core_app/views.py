from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django .http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)

def create_error_response(message, status_code):
     """
     This is a helper function to
     create a JSON response with an error message.
     """
     return JsonResponse({"error": message}, status=status_code)


@csrf_exempt
@api_view(['POST'])
def register_user(request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({"message": "User created"}, status=201)
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return create_error_response({"Error creating user"}, 500)

@csrf_exempt
@api_view(['POST'])
def login_user(request):
        try:
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
        except Exception as e:
            logger.error(f"Error logging in user: {str(e)}")
            return create_error_response({"Error logging in user"}, 500)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
        try:
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')

            task = Task.objects.create(user=request.user, title=title, description=description)
            return JsonResponse({'message': 'Task created successfully', 'task_id': task.id})
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            return create_error_response({"Error creating task"}, 500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tasks(request):
        try:
            tasks = Task.objects.filter(user=request.user).values('id', 'title', 'description', 'completed')
            return JsonResponse(list(tasks), safe=False)
        except Exception as e:
            logger.error(f"Error listing tasks: {str(e)}")
            return create_error_response({"Error listing tasks"}, 500)


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
    except Exception as e:
        logger.error(f"Error getting task: {str(e)}")
        return create_error_response({"Error getting task"}, 500)

@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
        try:
            data = json.loads(request.body)
            task = Task.objects.get(id=task_id, user=request.user)
            task.title = data.get("title", task.title)
            task.description = data.get("description", task.description)
            task.completed = data.get('completed', task.completed)
            task.save()

            return JsonResponse({"message": "Task updated"})
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
        except Exception as e:
            logger.error(f"Error updating task: {str(e)}")
            return create_error_response({"Error updating task"}, 500)
        
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.delete()
            return JsonResponse({"message": "Task deleted"})
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
        except Exception as e:
            logger.error(f"Error deleting task: {str(e)}")
            return create_error_response({"Error deleting task"}, 500)

@api_view(['POST'])        
def user_logout(request):
    try:
        logout(request)
        return JsonResponse({"message": "Logout successful"})
    except Exception as e:
        logger.error(f"Error logging out user: {str(e)}")
        return create_error_response({"Error logging out user"}, 500)