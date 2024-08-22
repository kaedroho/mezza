from django import forms

from ..models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "due_date",
            "description",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"variant": "large"}),
        }
