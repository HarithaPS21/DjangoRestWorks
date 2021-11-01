from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, role, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            role=role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            role=role,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    options = (
        ("admin", "admin"),
        ("employer","employer"),
        ("jobseeker","jobseeker")

    )
    role = models.CharField(max_length=30,choices=options,default="jobseeker")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role',"password"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class CompanyProfile(models.Model):
    company = models.OneToOneField(MyUser,on_delete=models.CASCADE,null=True)
    logo = models.ImageField(upload_to="images",null=True)
    company_name = models.CharField(max_length=50)
    company_description = models.CharField(max_length=150)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.company_name


class JobOpening(models.Model):
    company = models.ForeignKey(CompanyProfile,on_delete=models.CASCADE,null=True)
    position = models.CharField(max_length=50)
    job_description = models.CharField(max_length=200)
    experience = models.IntegerField()
    qualification = models.CharField(max_length=100)
    no_of_vacancies = models.IntegerField()
    last_date_to_apply = models.DateField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.position


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE,null=True)
    profile_pic = models.ImageField(upload_to="images",null=True)
    name = models.CharField(max_length=90)
    skills = models.CharField(max_length=120)
    resume = models.FileField(upload_to="images",null=True)

    def __str__(self):
        return self.name


class JobApplication:
    job = models.ForeignKey(JobOpening,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(JobSeekerProfile,on_delete=models.CASCADE,null=True)
    options = (
        ("applied","applied"),
        ("approved","approved"),
        ("rejected","rejected")
    )
    status = models.CharField(choices=options,default="applied")
    application_date = models.DateField()
