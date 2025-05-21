from rest_framework.viewsets import ModelViewSet
from .serializers import TodoSeralizer
from .models import Todo

class TodoViewSet(ModelViewSet):
    serializer_class = TodoSeralizer

    def get_queryset(self):
        status = self.request.query_params.get('status', '')
        search = self.request.query_params.get('search', '')

        if status == 'completed':
            queryset = Todo.objects.filter(is_completed=True)
        elif status == 'not-completed':
            queryset = Todo.objects.filter(is_completed=False)
        else:
            queryset = Todo.objects.all()

        if search:
            queryset = queryset.filter(task_name__icontains=search)
        return queryset