from django import forms


class AssetMetadataForm(forms.Form):
    title = forms.CharField(max_length=255)

    class Meta:
        fields = [
            "title",
        ]


class AssetUploadForm(AssetMetadataForm):
    file = forms.FileField()

    class Meta:
        fields = AssetMetadataForm.Meta.fields + [
            "file",
        ]
