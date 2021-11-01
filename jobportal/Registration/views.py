from django.views.generic import TemplateView,CreateView
from .models import MyUser
from Registration import forms
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


class EmployerHome(TemplateView):
    template_name = "Registration/employer_home.html"


class JobSeekerHome(TemplateView):
    template_name = "Registration/jobseeker_home.html"


class Registration(CreateView):
    model = MyUser
    form_class = forms.RegistrationForm
    template_name = "Registration/register.html"
    success_url = reverse_lazy("signin")


class Login(TemplateView):
    template_name = "Registration/signin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.LoginForm()
        context['form'] = form
        return context

    def post(self,request,*args,**kwargs):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request,user)
                if user.role=="employer":
                    return redirect("employerhome")
                else:
                    return redirect("jobseekerhome")
            else:
                return redirect("signin")


class Logout(TemplateView):

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")