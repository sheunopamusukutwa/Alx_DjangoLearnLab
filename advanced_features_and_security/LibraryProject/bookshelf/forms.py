from django import forms

class ExampleForm(forms.Form):
    """A simple example form to demonstrate CSRF protection and safe input handling."""
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your name"})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Write your message here..."}),
        required=True
    )