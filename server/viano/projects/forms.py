from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"variant": "large"}),
        }
