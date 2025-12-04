"""
URL configuration for embedding API endpoints.
"""

from django.urls import path

from embeddings.views import page_embeddings

urlpatterns = [
    path("<int:page_id>/embeddings/", page_embeddings, name="page_embeddings"),
]
