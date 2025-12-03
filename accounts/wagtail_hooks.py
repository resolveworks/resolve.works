from django.utils.translation import gettext_lazy as _

from wagtail import hooks
from wagtail.admin.panels import InlinePanel, ObjectList
from wagtail.admin.views.account import BaseSettingsPanel

from .forms import ProfileSettingsForm
from .models import User


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


class WorkExperienceSettingsPanel(BaseSettingsPanel):
    """Panel for editing work experience using Wagtail's InlinePanel."""

    name = "work_experience"
    title = _("Work experience")
    order = 250
    template_name = "accounts/account/work_experience_panel.html"

    def __init__(self, request, user, profile):
        super().__init__(request, user, profile)
        # Create the panel definition with InlinePanel
        self.edit_handler = ObjectList(
            [
                InlinePanel("work_experiences", label="Work experience"),
            ]
        ).bind_to_model(User)

    def get_form(self):
        form_class = self.edit_handler.get_form_class()
        kwargs = {
            "instance": self.user,
            "prefix": self.name,
        }

        if self.request.method == "POST":
            return form_class(self.request.POST, self.request.FILES, **kwargs)
        else:
            return form_class(**kwargs)

    def get_context_data(self):
        form = self.get_form()
        bound_panel = self.edit_handler.get_bound_panel(
            instance=self.user,
            request=self.request,
            form=form,
            prefix=self.name,
        )
        return {
            "form": form,
            "panel": bound_panel,
        }


@hooks.register("register_account_settings_panel")
def register_work_experience_panel(request, user, profile):
    return WorkExperienceSettingsPanel(request, user, profile)
