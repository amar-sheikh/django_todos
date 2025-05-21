from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib import admin
from .models import Todo

class TestTodoModel(TestCase):

    def test_create_todo(self):
        self.todo = Todo.objects.create(
            task_name='Task',
            task_description='Description',
            is_completed=True
        )

        self.todo.full_clean()
        self.assertEqual(self.todo.task_name, 'Task')
        self.assertEqual(self.todo.task_description, 'Description')
        self.assertTrue(self.todo.is_completed)
    
    def test_create_todo_with_task_name_blank(self):
        self.todo = Todo.objects.create(
            task_name='',
            task_description='Description',
            is_completed=True
        )

        with self.assertRaises(ValidationError) as context:
            self.todo.full_clean()
        self.assertIn('This field cannot be blank.', context.exception.message_dict['task_name'])
    
    def test_create_todo_with_none_task_name(self):
        with self.assertRaises(IntegrityError) as context:
            self.todo = Todo.objects.create(
                task_name=None,
                task_description='Description',
                is_completed=True
            )
        self.assertIn('NOT NULL constraint failed', str(context.exception))
        self.assertIn('app_todo.task_name', str(context.exception))

    def test_create_todo_with_without_task_name(self):
        self.todo = Todo.objects.create(
            task_description='Description',
            is_completed=True
        )

        with self.assertRaises(ValidationError) as context:
            self.todo.full_clean()
        self.assertIn('This field cannot be blank.', context.exception.message_dict['task_name'])

    def test_create_todo_with_shorter_task_name_length(self):
        self.todo = Todo.objects.create(
            task_name='T',
            task_description='Description',
            is_completed=True
        )

        with self.assertRaises(ValidationError) as context:
            self.todo.full_clean()
        self.assertIn('Ensure this value has at least 3 characters (it has 1).', context.exception.message_dict['task_name'])
    
    def test_create_todo_with_longer_task_name_length(self):
        self.todo = Todo.objects.create(
            task_name='Title: The task for with the length greater than 50',
            task_description='Description',
            is_completed=True
        )

        with self.assertRaises(ValidationError) as context:
            self.todo.full_clean()
        self.assertIn('Ensure this value has at most 50 characters (it has 51).', context.exception.message_dict['task_name'])
    
    def test_create_todo_with_task_name_already_exist(self):
        Todo.objects.create(
            task_name='Task',
            task_description='Description',
            is_completed=True
        )

        self.todo = Todo.objects.create(
            task_name='Task',
            task_description='',
            is_completed=False
        )

        with self.assertRaises(ValidationError) as context:
            self.todo.full_clean()
        self.assertIn('Todo with this Task name already exists.', context.exception.message_dict['task_name'])

    def test_create_todo_without_description(self):
        self.todo = Todo.objects.create(
            task_name='Task',
            is_completed=False
        )

        self.todo.full_clean()
        self.assertEqual(self.todo.task_name, 'Task')
        self.assertIsNone(self.todo.task_description)
        self.assertFalse(self.todo.is_completed)

    def test_create_todo_without_is_completed(self):
        self.todo = Todo.objects.create(
            task_name='Task',
            task_description='Description',
        )

        self.todo.full_clean()
        self.assertEqual(self.todo.task_name, 'Task')
        self.assertEqual(self.todo.task_description, 'Description')
        self.assertFalse(self.todo.is_completed)

class TestTodoAdmin(TestCase):
    def setUp(self):
        self.todo_admin = admin.site._registry[Todo]

    def test_display_list(self):
        self.assertEqual(self.todo_admin.list_display, ('id', 'task_name', 'is_completed'))
    
    def test_list_filter(self):
        self.assertEqual(self.todo_admin.list_filter, ['is_completed'])
    
    def test_search_fields(self):
        self.assertEqual(self.todo_admin.search_fields, ('task_name', 'task_description'))

class TodoViewSet(TestCase):
    def setUp(self):
        self.not_completed_task = Todo.objects.create(
            task_name='Task 1',
            task_description='Task 1 description',
            is_completed=False
        )
        self.completed_task = Todo.objects.create(
            task_name='Task 2',
            task_description='Task 2 description',
            is_completed=True
        )

    def test_todo_list_view_without_filter(self):
        self.assertEqual(Todo.objects.count(), 2)

        response = self.client.get(reverse('todo-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        data = response.json()
        self.assertEqual(data['count'], 2)
        self.assertEqual(data['results'][0]['id'], self.not_completed_task.id)
        self.assertEqual(data['results'][1]['id'], self.completed_task.id)

    def test_todo_list_view_with_status_filter(self):
        self.assertEqual(Todo.objects.count(), 2)

        response = self.client.get(reverse('todo-list'), {
            'status': 'completed'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['id'], self.completed_task.id)

    def test_todo_list_view_with_search_and_status_filter(self):
        self.not_completed_task_2 = Todo.objects.create(
            task_name='Todo 1',
            task_description='Todo 1 description',
            is_completed=False
        )
        self.completed_task_2 = Todo.objects.create(
            task_name='Todo 2',
            task_description='Todo 2 description',
            is_completed=True
        )

        self.assertEqual(Todo.objects.count(), 4)

        response = self.client.get(reverse('todo-list'), {
            'search': 'task',
            'status': 'not-completed'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['id'], self.not_completed_task.id)

    def test_todo_get_view(self):
        response = self.client.get(reverse('todo-detail', args=[self.not_completed_task.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertContains(response, self.not_completed_task)
        self.assertNotContains(response, self.completed_task)

    def test_todo_get_view_with_invalid_id(self):
        response = self.client.get(reverse('todo-detail', args=[self.completed_task.id + 1]))

        self.assertEqual(response.status_code, 404)

    def test_todo_create_view(self):
        data = {
            'task_name': 'Task 3',
            'task_description': 'Task 3 description',
            'is_completed': False
        }

        self.assertEqual(Todo.objects.count(), 2)

        response = self.client.post(reverse('todo-list'), data=data)

        self.assertEqual(Todo.objects.count(), 3)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data['task_name'], 'Task 3')
        self.assertEqual(response.data['task_description'], 'Task 3 description')
        self.assertEqual(response.data['is_completed'], False)

    def test_todo_create_view_with_invalid_data(self):
        data = {
            'task_name': 'Task 1',
            'task_description': 'Task 3 description',
            'is_completed': False
        }

        self.assertEqual(Todo.objects.count(), 2)

        response = self.client.post(reverse('todo-list'), data=data)

        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertIn('todo with this task name already exists.', response.data['task_name'])

    def test_todo_update_view(self):
        data = {
            'id': self.not_completed_task.id,
            'task_name': 'Updated task name',
            'task_description': 'Updated task description',
            'is_completed': True
        }

        self.assertEqual(self.not_completed_task.task_name, 'Task 1')
        self.assertEqual(self.not_completed_task.task_description, 'Task 1 description')
        self.assertFalse(self.not_completed_task.is_completed)

        response = self.client.put(reverse('todo-detail', args=[self.not_completed_task.id]), data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.not_completed_task.refresh_from_db()
        self.assertEqual(self.not_completed_task.task_name, 'Updated task name')
        self.assertEqual(self.not_completed_task.task_description, 'Updated task description')
        self.assertTrue(self.not_completed_task.is_completed)

    def test_todo_update_view_with_invalid_data(self):
        data = {
            'id': self.not_completed_task.id,
            'task_name': '',
            'task_description': 'Updated task description',
            'is_completed': True
        }

        self.assertEqual(self.not_completed_task.task_name, 'Task 1')
        self.assertEqual(self.not_completed_task.task_description, 'Task 1 description')
        self.assertFalse(self.not_completed_task.is_completed)

        response = self.client.put(reverse('todo-detail', args=[self.not_completed_task.id]), data=data, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertIn('This field may not be blank.', response.data['task_name'])
        self.not_completed_task.refresh_from_db()
        self.assertEqual(self.not_completed_task.task_name, 'Task 1')
        self.assertEqual(self.not_completed_task.task_description, 'Task 1 description')
        self.assertFalse(self.not_completed_task.is_completed)

    def test_todo_delete_view(self):
        self.assertEqual(Todo.objects.count(), 2)

        response = self.client.delete(reverse('todo-detail', args=[self.not_completed_task.id]))

        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(response.status_code, 204)

    def test_todo_delete_view_with_invalid_id(self):
        self.assertEqual(Todo.objects.count(), 2)

        response = self.client.delete(reverse('todo-detail', args=[self.completed_task.id + 1]))

        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(response.status_code, 404)