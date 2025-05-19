from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo

class TodoList(ListView):
    model=Todo
    template_name='todo/list.html'
    context_object_name='todos'

    def get_queryset(self):
        status = self.request.GET.get('status', 'completed')
        search = self.request.GET.get('search', '')

        if status == 'all':
            queryset = Todo.objects.all()
        elif status == 'not_completed':
            queryset = Todo.objects.filter(is_completed=False)
        else:
            queryset = Todo.objects.filter(is_completed=True)

        if search:
            queryset = queryset.filter(task_name__icontains=search)
        return queryset
class TodoCreate(CreateView):
    model=Todo
    fields = ["task_name", "task_description", "is_completed"]
    template_name='todo/form.html'
    success_url=reverse_lazy('todo_list')

class TodoUpdate(UpdateView):
    model=Todo
    fields = ["task_name", "task_description", "is_completed"]
    template_name='todo/form.html'
    success_url=reverse_lazy('todo_list')

class TodoDelete(DeleteView):
    model=Todo
    template_name='todo/confirm_delete.html'
    success_url=reverse_lazy('todo_list')