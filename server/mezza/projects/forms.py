from django import forms

from mezza.models import Project
from mezza.widgets import BlockNoteEditor


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


class ProjectScriptForm(forms.ModelForm):
    script = forms.JSONField(required=False, widget=BlockNoteEditor())

    class Meta:
        model = Project
        fields = [
            "script",
        ]
