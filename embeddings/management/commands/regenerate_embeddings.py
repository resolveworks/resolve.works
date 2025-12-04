"""
Management command to regenerate embedding visualizations for all pages.
"""

from django.core.management.base import BaseCommand

from embeddings.models import EmbeddingMixin


class Command(BaseCommand):
    help = "Regenerate embedding visualizations for all published pages with EmbeddingMixin"

    def handle(self, *args, **options):
        from wagtail.models import Page

        count = 0
        for page in Page.objects.live().specific():
            if isinstance(page, EmbeddingMixin):
                self.stdout.write(f"Generating embeddings for: {page.title}")
                page.generate_embedding_visualization()
                type(page).objects.filter(pk=page.pk).update(
                    embedding_visualization=page.embedding_visualization
                )
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully regenerated embeddings for {count} pages")
        )
