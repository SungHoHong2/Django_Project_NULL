from django import forms
from member.models import MyUser

class LoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class' : 'form-control'}),
            'password': forms.PasswordInput(attrs={'class' : 'form-control'}),
        }



