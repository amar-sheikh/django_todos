from rest_framework import serializers
from .models import Todo

class TodoSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
