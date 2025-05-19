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

class TestTodoListViews(TestCase):
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
        response = self.client.get(reverse('todo_list'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.not_completed_task)
        self.assertContains(response, self.completed_task)

    def test_todo_list_view_with_status_completed(self):
        response = self.client.get(reverse('todo_list'), data={'status': 'completed'})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.not_completed_task)
        self.assertContains(response, self.completed_task)

    def test_todo_list_view_with_status_not_completed(self):
        response = self.client.get(reverse('todo_list'), data={'status': 'not_completed'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.not_completed_task)
        self.assertNotContains(response, self.completed_task)

    def test_todo_list_view_with_status_all(self):
        response = self.client.get(reverse('todo_list'), data={'status': 'all'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.not_completed_task)
        self.assertContains(response, self.completed_task)

    def test_todo_list_view_with_invalid_status(self):
        response = self.client.get(reverse('todo_list'), data={'status': 'xyz'})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.not_completed_task)
        self.assertContains(response, self.completed_task)

    def test_todo_list_view_with_a_search_matching_any_todo_task_name(self):
        task_not_in_matching_search = Todo.objects.create(
            task_name='Todo 1',
            task_description='Task 2 description',
            is_completed=True
        )

        response = self.client.get(reverse('todo_list'), data={'status': 'all', 'search': 'Task'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.not_completed_task)
        self.assertContains(response, self.completed_task)
        self.assertNotContains(response, task_not_in_matching_search)

    def test_todo_list_view_with_a_search_not_matching_any_todo_task_name(self):
        response = self.client.get(reverse('todo_list'), data={'status': 'all', 'search': 'Todo'})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.not_completed_task)
        self.assertNotContains(response, self.completed_task)

    def test_todo_list_view_with_a_search_not_matching_in_todo_task_name_filtered_by_status(self):
        response = self.client.get(reverse('todo_list'), data={'status': 'completed', 'search': 'task 1'})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.not_completed_task)
        self.assertNotContains(response, self.completed_task)

class TestTodoCreateViews(TestCase):
    def setUp(self):
        self.todo1 = Todo.objects.create(
            task_name='Task 1',
            task_description='Task 1 description',
            is_completed=False
        )

    def test_get_create_view(self):
        response = self.client.get(reverse('todo_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_todo_create_view(self):
        data = {
            "task_name": 'Task 2',
            "task_description": 'Task 2 description',
            "is_completed": True
        }
        self.assertEqual(Todo.objects.count(), 1)

        response = self.client.post(reverse('todo_create'), data)

        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))
        last_todo = Todo.objects.last()
        self.assertEqual(last_todo.task_name, 'Task 2')
        self.assertEqual(last_todo.task_description, 'Task 2 description')
        self.assertTrue(last_todo.is_completed)

    def test_post_todo_create_view_with_invalid_data(self):
        data = {
            "task_name": 'Task 1',
            "task_description": 'Task 2 description',
            "is_completed": True
        }
        self.assertEqual(Todo.objects.count(), 1)

        response = self.client.post(reverse('todo_create'), data)

        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Todo with this Task name already exists.', response.context['form'].errors['task_name'])

class TestTodoUpdateView(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            task_name='Task name',
            task_description='Task description',
            is_completed=True
        )

    def test_get_todo_update_view(self):
        response = self.client.get(reverse('todo_edit', args=[self.todo.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_todo_update_view_with_invalid_id(self):
        response = self.client.get(reverse('todo_edit', args=[self.todo.id + 1]))
        self.assertEqual(response.status_code, 404)

    def test_post_todo_update_view(self):
        data = {
            "task_name": 'New task name',
            "task_description": 'New task description',
            "is_completed": False
        }

        self.assertEqual(self.todo.task_name, 'Task name')
        self.assertEqual(self.todo.task_description, 'Task description')
        self.assertTrue(self.todo.is_completed)

        response = self.client.post(reverse('todo_edit', args=[self.todo.id]), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.task_name, 'New task name')
        self.assertEqual(self.todo.task_description, 'New task description')
        self.assertFalse(self.todo.is_completed)

    def test_post_todo_update_view_with_invalid_data(self):
        data = {
            "task_name": '',
            "task_description": 'New task description',
            "is_completed": False
        }

        self.assertEqual(self.todo.task_name, 'Task name')
        self.assertEqual(self.todo.task_description, 'Task description')
        self.assertTrue(self.todo.is_completed)

        response = self.client.post(reverse('todo_edit', args=[self.todo.id]), data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('This field is required.', response.context['form'].errors['task_name'])
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.task_name, 'Task name')
        self.assertEqual(self.todo.task_description, 'Task description')
        self.assertTrue(self.todo.is_completed)

class TestTodoDeleteView(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            task_name='Task name',
            task_description='Task description',
            is_completed=True
        )

    def test_get_todo_delete_view(self):
        response = self.client.get(reverse('todo_delete', args=[self.todo.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_todo_delete_view_with_invalid_id(self):
        response = self.client.get(reverse('todo_delete', args=[self.todo.id + 1]))
        self.assertEqual(response.status_code, 404)

    def test_post_todo_delete_view(self):
        self.assertEqual(Todo.objects.count(), 1)

        response = self.client.post(reverse('todo_delete', args=[self.todo.id]))

        self.assertEqual(Todo.objects.count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))

    def test_post_todo_delete_view_with_invalid_id(self):
        self.assertEqual(Todo.objects.count(), 1)

        response = self.client.post(reverse('todo_delete', args=[self.todo.id + 1]))

        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(response.status_code, 404)