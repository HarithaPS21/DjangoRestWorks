from django.urls import path
from Registration import views

urlpatterns = [
    path("accounts/register", views.Registration.as_view(), name="signup"),
    path("accounts/login", views.Login.as_view(),name="signin"),
    path("accounts/logout", views.Logout.as_view(), name="signout"),

    path("home", views.EmployerHome.as_view(), name="employerhome"),
    path("", views.JobSeekerHome.as_view(), name="jobseekerhome"),


]