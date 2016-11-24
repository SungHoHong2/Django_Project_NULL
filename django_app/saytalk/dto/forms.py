from django import forms

from collection.models import Image
from saytalk.models import SayTalk

class PostInsertForm(forms.ModelForm):
    class Meta:
        model = SayTalk
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
        }

class PostImageForm(forms.ModelForm):
    img_file = forms.ImageField(label='', widget= forms.FileInput(attrs={'class' : 'form-control'}))
    class Meta:
        model = Image
        fields = ('img_file',)