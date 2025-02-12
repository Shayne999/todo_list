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
@permission_classes([IsAuthenticated]) #ensures only an admin can create another
def register_user(request):
        """
            Allows users to create accounts.
            Only admin users to create other admin accounts
        """
        try:
            if not request.user.is_staff:
                 return JsonResponse(
                      {"error": "Only admins can create new users"},
                      status=403
                )
            
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            is_admin = data.get('is_admin', False)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User.objects.create_user(username=username, password=password)
            if is_admin:
                 user.is_staff = True
                 user.save()

            return JsonResponse({"message": "User created"}, status=201)
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return create_error_response({"Error creating user"}, 500)

@csrf_exempt
@api_view(['POST'])
def login_user(request):
        """Handles user login"""

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
        """Handles task creation"""

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
        """Lists all the tasks available.
        admin/staff users can see all tasks while
        non admin users will only see their own tasks
        """
        try:
            if request.user.is_staff:
                tasks = Task.objects.all().values(
                     'id', 'title', 'description',
                     'completed', 'user__username'
                     )
            else:
                tasks = Task.objects.filter(user=request.user).values(
                     'id', 'title', 'description', 'completed')
                
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
        return create_error_response({"error": "Error getting task"}, 500)


@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
        """
            Allows users to update tasks
        """
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
        """
            Allows admin users to delete all tasks.
            Non admin users are resticted to their own tasks
        """
        try:
            if request.user.is_staff:
                task = Task.objects.get(id=task_id)
            else:
                task = Task.objects.get(id=task_id, user=request.user)

            task.delete()
            return JsonResponse({"message": "Task Deleted"})
        
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