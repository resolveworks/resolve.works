"""
API views for embedding visualization.
"""

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from wagtail.models import Page

from embeddings.models import EmbeddingMixin


@require_GET
def page_embeddings(request, page_id):
    """
    API endpoint to fetch embedding visualization data for any page.

    Returns JSON with nodes and edges arrays for visualization.
    """
    try:
        page = Page.objects.get(pk=page_id).specific
    except Page.DoesNotExist:
        return JsonResponse({"error": "Page not found"}, status=404)

    if not isinstance(page, EmbeddingMixin):
        return JsonResponse({"error": "Page does not support embeddings"}, status=400)

    if not page.live:
        return JsonResponse({"error": "Page not published"}, status=404)

    data = page.embedding_visualization or {"nodes": [], "edges": []}

    response = JsonResponse(data)
    response["Cache-Control"] = "public, max-age=3600"
    return response
