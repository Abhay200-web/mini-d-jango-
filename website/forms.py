from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = ''


class AddRecordForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label=""
    )

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}), label="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}), label="")
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}), label="")
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}), label="")
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}), label="")
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}), label="")
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State'}), label="")
    pincode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Pincode'}), label="")

    class Meta:
        model = Record
        fields = "__all__"
