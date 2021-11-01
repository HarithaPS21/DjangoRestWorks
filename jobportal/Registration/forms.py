from Registration.admin import UserCreationForm
from Registration.models import MyUser
from django import forms


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model = MyUser
        fields = ["email", "role", "password1", "password2"]
        widgets ={
            "email" : forms.TextInput(attrs={"class":"form-control"}),
            "role" : forms.Select(attrs={"class":"form-select"})
        }
        labels = {
            "password1" : "Password",
            "password2" : "Confirm Password"
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data["email"]
        users = MyUser.objects.filter(email=email)
        if users:
            msg = "The user already exists"
            self.add_error("email",msg)


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))



