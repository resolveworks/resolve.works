from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with additional profile fields."""

    job_title = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    profile_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )


class WorkExperience(models.Model):
    """Work experience entry for a user."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="work_experiences",
    )
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Leave blank if current position",
    )

    class Meta:
        ordering = ["-start_year"]

    def __str__(self):
        return f"{self.role} at {self.company}"

    @property
    def date_range(self):
        if self.end_year:
            return f"{self.start_year}–{self.end_year}"
        return f"{self.start_year}–present"
