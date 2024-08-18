from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task #el formulario se basara en este modelo task
        fields = ["title", "description", "important"] #estos seran los campos de los formularios a enviar
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control', "placeholder": "Wirte a title"}),
            "description": forms.Textarea(attrs={'class': 'form-control', "placeholder": "Write a description"}),
            "important": forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'})
        }