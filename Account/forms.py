from django import forms
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class SigninForm(forms.Form):
    # User login form
    username = forms.CharField()
    password = forms.CharField()
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)  # Captcha for user login


class SignupForm(forms.ModelForm):
    # User registration form
    confirm_password = forms.CharField(min_length=8)  # pass2

    class Meta:
        model = CustomUser
        # Form fields
        fields = ['username', 'email', 'first_name', 'last_name', 'image', 'password', 'phone_number',
                  'confirm_password']

    def clean_confirm_password(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


'''
Classes related to creating a custom user
                ||
                \/
'''


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser  # model user customize
        fields = UserCreationForm.Meta.fields + ('image',) + ('national_number',) + ('card_number',) + ('phone_number',)


class CustomUserUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser  # model user customize
        fields = UserChangeForm.Meta.fields
