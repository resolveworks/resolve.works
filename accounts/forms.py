from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserCreationForm, UserEditForm

User = get_user_model()


class CustomUserEditForm(UserEditForm):
    """Custom user edit form with additional profile fields."""

    job_title = forms.CharField(max_length=100, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    linkedin_url = forms.URLField(required=False, label="LinkedIn URL")
    github_url = forms.URLField(required=False, label="GitHub URL")
    phone = forms.CharField(max_length=50, required=False)


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with additional profile fields."""

    job_title = forms.CharField(max_length=100, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    linkedin_url = forms.URLField(required=False, label="LinkedIn URL")
    github_url = forms.URLField(required=False, label="GitHub URL")
    phone = forms.CharField(max_length=50, required=False)


class ProfileSettingsForm(forms.ModelForm):
    """Form for user profile settings on the account page."""

    class Meta:
        model = User
        fields = [
            "job_title",
            "bio",
            "linkedin_url",
            "github_url",
            "phone",
        ]
        labels = {
            "job_title": _("Job title"),
            "bio": _("Bio"),
            "linkedin_url": _("LinkedIn URL"),
            "github_url": _("GitHub URL"),
            "phone": _("Phone"),
        }
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
