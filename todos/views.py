from accounts.models import User
from todos.serializers import TodoSerializer
from .models import Todo
from rest_framework import permissions, generics, status, mixins, viewsets
from rest_framework.decorators import action

class TodoViewSet(viewsets.ModelViewSet):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = TodoSerializer
  queryset = Todo.objects.all()

  def get_queryset(self):
    return Todo.objects.filter(author=self.request.user)
  
  def perform_create(self, serializer):
    serializer.save(author=self.request.user)

	### 추가하기 ###
  @action(detail=True, methods=['patch'])
  def check(self, request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.check_todo()
    serializer = self.serializer_class(todo)
    return Response(serializer.data, status=status.HTTP_200_OK)
