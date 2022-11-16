from django.test import TestCase
from accounts.models import User
from .models import Todo
from .serializers import TodoSerializer
import json
from rest_framework.test import APIClient, APITestCase

# Create your tests here.
class TestTodos(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username = 'test', password = '12345678')
        self.client.force_authenticate(user = self.user)

    def test_get_todos(self):
        # create a todo
        Todo.objects.create(author = self.user, text = "test1")
        Todo.objects.create(author = self.user, text = "test2")
        Todo.objects.create(author = self.user, text = "test3")
        serializer = TodoSerializer(Todo.objects.filter(author=self.user), many = True)
        url = "/api/todos/"
        response = self.client.get(url)
        print(serializer.data)
        print(response.json())
        # self.assertEqual(serializer.data, response.json())
        self.assertEqual(serializer.data, "")
        self.assertEqual(200, response.status_code)
    
    def test_post_todos(self):
        url = "/api/todos/"
        data = { "text": "test" }
        response = self.client.post(url, data)
        self.assertEqual(201, response.status_code)
