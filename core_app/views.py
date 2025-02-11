from django .http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Task


@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.create(
            task=data['task'],
            description=data['description'],
            completed=data.get('completed', False),
        )
        return JsonResponse({"message": "Task created", "task_id": task.id})
    
def get_tasks(request):
    """
    Retrieves all tasks.
    """
    tasks = list(Task.objects.values())
    return JsonResponse(tasks, safe=False)

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