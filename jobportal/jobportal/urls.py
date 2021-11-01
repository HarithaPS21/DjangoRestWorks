from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jobportal/', include('Registration.urls')),
    path('employer/', include('Employer.urls')),

]
