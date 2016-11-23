from django import forms
from member.models import MyUser
from collection.models import Image

class LoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class' : 'form-control'}),
            'password': forms.PasswordInput(attrs={'class' : 'form-control'}),
        }

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='nickname', widget= forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(label='phone_number', widget= forms.PasswordInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = MyUser
        fields = ('username', 'password', )

class RegisterImageForm(forms.ModelForm):
    img_file = forms.ImageField(label='', widget= forms.FileInput(attrs={'class' : 'form-control'}))
    class Meta:
        model = Image
        fields = ('img_file',)


