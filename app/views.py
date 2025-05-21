from rest_framework.viewsets import ModelViewSet
from .serializers import TodoSeralizer
from .models import Todo

class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSeralizer
