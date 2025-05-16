from django.test import TestCase
from django.core.exceptions import ValidationError
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