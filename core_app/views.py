from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django .http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Task


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User created"}, status=201)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"message": "Login successful"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)


@csrf_exempt
def create_task(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')

        task = Task.objects.create(user=request.user, title=title, description=description)
        return JsonResponse({'message': 'Task created successfully', 'task_id': task.id})

    return JsonResponse({'error': 'Unauthorized'}, status=401)
    

@csrf_exempt
def list_tasks(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).values('id', 'title', 'description', 'completed')
        return JsonResponse(list(tasks), safe=False)

    return JsonResponse({'error': 'Unauthorized'}, status=401)

def get_task(request, task_id):
    """
    Retrieves a specific task by ID.
    """
    try:
        task = Task.objects.get(id=task_id)
        return JsonResponse({
            "task": task.task,
            "description": task.description,
            "completed": task.completed,
        })
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

@csrf_exempt
def update_task(request, task_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            task = Task.objects.get(id=task_id)
            task.task = data.get("task", task.task)
            task.description = data.get("description", task.description)
            task.completed = data.get('completed', task.completed)
            task.save()

            return JsonResponse({"message": "Task updated"})
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
        
@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'DELETE':
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return JsonResponse({"message": "Task deleted"})
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
        
def user_logout(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"})