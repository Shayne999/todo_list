from django.test import TestCase
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Task
import json

class TaskAPITest(TestCase):
    def setUp(self):
        """Set up test client and create a test user."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
    
    def test_user_registration(self):
        """Test user registration endpoint."""
        response = self.client.post("/register/", json.dumps({
            "username": "newuser",
            "password": "newpassword"
        }), content_type="application/json")
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created", response.json()["message"])

    def test_user_login(self):
        """Test login endpoint."""
        response = self.client.post("/login/", json.dumps({
            "username": "testuser",
            "password": "testpassword"
        }), content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login successful", response.json()["message"])
    
    def test_create_task(self):
        """Test creating a task when authenticated."""
        self.client.login(username="testuser", password="testpassword")  # Authenticate user
        
        response = self.client.post("/tasks/create/", json.dumps({
            "title": "Test Task",
            "description": "This is a test task."
        }), content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Task created successfully", response.json()["message"])

    def test_list_tasks(self):
        """Test listing tasks for authenticated user."""
        self.client.login(username="testuser", password="testpassword")
        
        # Create a task first
        Task.objects.create(user=self.user, title="Sample Task", description="Task description")
        
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_update_task(self):
        """Test updating a task."""
        self.client.login(username="testuser", password="testpassword")
        
        task = Task.objects.create(user=self.user, title="Old Title", description="Old description")
        
        response = self.client.put(f"/tasks/{task.id}/update/", json.dumps({
            "title": "Updated Task",
            "description": "Updated description",
            "completed": True
        }), content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Task updated", response.json()["message"])

    def test_delete_task(self):
        """Test deleting a task."""
        self.client.login(username="testuser", password="testpassword")
        
        task = Task.objects.create(user=self.user, title="Task to Delete", description="To be deleted")
        
        response = self.client.delete(f"/tasks/{task.id}/delete/")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Task deleted", response.json()["message"])
    
    def test_user_logout(self):
        """Test user logout."""
        self.client.login(username="testuser", password="testpassword")
        
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Logout successful", response.json()["message"])

