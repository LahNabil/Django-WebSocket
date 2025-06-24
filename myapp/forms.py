# myapp/forms.py

from django import forms
from .models import TaskItem

class TaskItemForm(forms.ModelForm):
    """
    A form for creating and updating TaskItem instances.
    It automatically generates form fields based on the TaskItem model.
    """
    class Meta:
        model = TaskItem
        fields = ['title', 'description', 'completed'] # Fields to include in the form
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Task Description (optional)'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Task Title',
            'description': 'Description',
            'completed': 'Is Completed?'
        }
