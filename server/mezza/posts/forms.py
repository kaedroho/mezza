from django import forms

from ..widgets import BlockNoteEditor
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"variant": "large"}),
            "content": BlockNoteEditor(),
        }
