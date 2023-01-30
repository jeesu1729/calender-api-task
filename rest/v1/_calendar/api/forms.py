from django import forms

class CredsForm(forms.Form):
    creds = forms.CharField(label='Paste your entire credentials.json here', max_length=1000)