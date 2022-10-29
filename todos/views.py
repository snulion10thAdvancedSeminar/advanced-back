import json
from django.views.generic import View

from accounts.models import User
from .models import Todo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import permissions, generics, mixins
from .serializers import TodoSerializer


def todo_instance_to_dictionary(todo):
  """
  장고 단일 모델 인스턴스, 혹은 쿼리셋을 파이썬 딕셔너리로 변환하는 헬퍼 함수
  """
  result = {}
  result["id"] = todo.id
  result["text"] = todo.text
  result["done"] = todo.done
  return result

class ViewWithoutCSRFAuthentication(generics.GenericAPIView):
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super(ViewWithoutCSRFAuthentication, self).dispatch(request, *args, **kwargs)

class TodoListView(generics.ListAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = TodoSerializer

  def get(self, request):
    try:
      # todo_list = []
      # todo_queryset = Todo.objects.filter(author_id = request.user.id)
      # for todo_instance in todo_queryset:
      #   todo_list.append(todo_instance_to_dictionary(todo_instance))
      # serializer = TodoSerializer(data=todo_queryset, many=True)
      # data = { "todos": serializer.data }
      # return JsonResponse(data, status=200)
      return self.list(request.data, status=200)
    except:
      return JsonResponse({"msg": "Failed to get todos"}, status=404)

class TodoCreateView(ViewWithoutCSRFAuthentication, generics.CreateAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = TodoSerializer

  def post(self, request):
    # try:
    #   body = json.loads(request.body) #body에서 받아온 것을 역직렬화!
    # except:
    #   return JsonResponse({"msg": "Invalid parameters"}, status=400)

    # try:
    #   todo_instance = Todo.objects.create(text=body["text"], author_id = request.user.id)
    # except:
    #   return JsonResponse({"msg": "Failed to create todos"}, status=400)

    # todo_dict = todo_instance_to_dictionary(todo_instance)
    # data = { "todo": serializer.data }
    # return JsonResponse(data, status=200)
    try:
      return self.create(request.data, status=200)
    except:
      return JsonResponse({"msg": "Failed to create todos"}, status=400)
    

class TodoCheckView(ViewWithoutCSRFAuthentication):
  permission_classes = [permissions.IsAuthenticated]

  def patch(self, request, id):
    try:
      # todo_instance = Todo.objects.get(id=id)
      # if (todo_instance.author_id != request.user.id):
      #   return JsonResponse({"msg": "Cannot access other's todo"}, status=401)
      # todo_instance.check_todo()
      # todo_dict = todo_instance_to_dictionary(todo_instance)
      # data = { "todo": todo_dict }
      # return JsonResponse(data, status=200)
      return self.update(request.data, id, status=200)
    except:
      return JsonResponse({"msg": "Failed to create todos"}, status=400)

class TodoView(ViewWithoutCSRFAuthentication, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = TodoSerializer

  def get(self, request, id):
    try:
      todo_instance = Todo.objects.get(id=id)

      if (todo_instance.author.id != request.user.id):
        return JsonResponse({"msg": "Cannot access other's todo"}, status=401)

      # todo_dict = todo_instance_to_dictionary(todo_instance)
      # data = { "todo": todo_dict }
      return self.retrieve(request, status=200)

    except:
      return JsonResponse({"msg": "Failed to get todo"}, status=404)

  def patch(self, request, id):
    try:
      # body = json.loads(request.body)
      body = request.data
    except:
      return JsonResponse({"msg": "Invalid parameters"}, status=400)

    try:
      todo_instance = Todo.objects.get(id=id)
      if (todo_instance.author.id != request.user.id):
        return JsonResponse({"msg": "Cannot access other's todo"}, status=401)

      # todo_instance.text = body["text"]
      # todo_instance.save()
      # todo_dict = todo_instance_to_dictionary(todo_instance)
      # data = { "todo": todo_dict }
      # return JsonResponse(data, status=200)
      return self.update(request, status=200)
    except:
      return JsonResponse({"msg": "Failed to edit todo"}, status=404)
  
  def delete(self, request, id):
    try:
      todo_instance = Todo.objects.get(id=id)

      if (todo_instance.author.id != request.user.id):
        return JsonResponse({"msg": "Cannot access other's todo"}, status=401)

      # todo_dict = todo_instance_to_dictionary(todo_instance)
      # todo_instance.delete()
      # data = { "todo": todo_dict }
      # return JsonResponse(data, status=200)
      return self.delete(request, id)
    except:
      return JsonResponse({"msg": "Failed to delete todo"}, status=404)
