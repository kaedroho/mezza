from django import forms

from mezza.models import Idea


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = [
            "title",
            "description",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"variant": "large"}),
        }
