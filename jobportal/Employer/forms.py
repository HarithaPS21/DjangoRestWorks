from django.forms import ModelForm
from Registration.models import MyUser, CompanyProfile
from django import forms


class AddCompanyProfileForm(ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ["company_name", "company_description", "location"]
        widgets = {
            "company_name" : forms.TextInput(attrs={"class":"form-control"}),
            "company_description" : forms.TextInput(attrs={"class":"form-control"}),
            "location": forms.TextInput(attrs={"class":"form-control"})
        }
        labels = {
            "company_name" : "Company Name" ,
            "company_description" : "Company Description" ,
            "location" : "Location"
        }