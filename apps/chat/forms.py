from django import forms


class MessageForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control mb-2", "rows": 2})
    )
