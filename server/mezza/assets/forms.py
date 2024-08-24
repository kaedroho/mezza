from django import forms


class AssetUploadForm(forms.Form):
    title = forms.CharField(max_length=255)
    file = forms.FileField()

    class Meta:
        fields = [
            "title",
            "file",
        ]
