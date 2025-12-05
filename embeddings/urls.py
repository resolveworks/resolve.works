"""
URL configuration for embedding API endpoints.
"""

from django.urls import path

from embeddings.views import page_embeddings

urlpatterns = [
    path("embeddings/", page_embeddings, name="page_embeddings"),
]
