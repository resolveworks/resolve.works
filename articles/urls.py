from django.urls import path

from articles.views import article_embeddings

urlpatterns = [
    path("<int:page_id>/embeddings/", article_embeddings, name="article_embeddings"),
]
