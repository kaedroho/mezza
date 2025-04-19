from django import forms


class FileMetadataForm(forms.Form):
    name = forms.CharField(max_length=255)

    class Meta:
        fields = [
            "name",
        ]


class FileUploadForm(forms.Form):
    file = forms.FileField()

    class Meta:
        fields = [
            "file",
        ]
