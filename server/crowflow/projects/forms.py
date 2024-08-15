from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    def __init__(self, space, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["flow"].queryset = space.flows.all()
        self.fields["stage"].queryset = space.stages.all()

    class Meta:
        model = Project
        fields = [
            "title",
            "flow",
            "stage",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"variant": "large"}),
        }
        labels = {"flow": "Type"}
