from django.utils.translation import gettext_lazy as _

from wagtail import hooks
from wagtail.admin.views.account import BaseSettingsPanel

from .forms import ProfileSettingsForm


class ProfileSettingsPanel(BaseSettingsPanel):
    """Panel for editing custom user profile fields."""

    name = "profile_settings"
    title = _("Profile details")
    order = 200
    form_class = ProfileSettingsForm
    form_object = "user"


@hooks.register("register_account_settings_panel")
def register_profile_settings_panel(request, user, profile):
    return ProfileSettingsPanel(request, user, profile)
