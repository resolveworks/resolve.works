"""
API views for embedding visualization.
"""

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from wagtail.models import Page

from embeddings.models import EmbeddingMixin


@require_GET
def page_embeddings(request):
    """
    API endpoint to fetch embedding visualization data for pages.

    Accepts comma-separated page IDs via the 'ids' query parameter.
    Returns JSON with embedding data keyed by page ID.

    Example: /api/pages/embeddings/?ids=1,2,3
    Returns: {"1": {"nodes": [...], "edges": [...], "hue": 200}, "2": {...}}
    """
    ids_param = request.GET.get("ids", "")
    if not ids_param:
        return JsonResponse({"error": "Missing 'ids' parameter"}, status=400)

    try:
        page_ids = [int(pid.strip()) for pid in ids_param.split(",") if pid.strip()]
    except ValueError:
        return JsonResponse({"error": "Invalid page ID format"}, status=400)

    if not page_ids:
        return JsonResponse({"error": "No valid page IDs provided"}, status=400)

    pages = Page.objects.filter(pk__in=page_ids).specific()

    result = {}
    for page in pages:
        if isinstance(page, EmbeddingMixin) and page.live:
            result[str(page.pk)] = page.embedding_visualization or {
                "nodes": [],
                "edges": [],
            }

    response = JsonResponse(result)
    response["Cache-Control"] = "public, max-age=3600"
    return response
