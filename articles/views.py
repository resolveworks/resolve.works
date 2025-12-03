from django.http import JsonResponse
from django.views.decorators.http import require_GET

from wagtail.models import Page


@require_GET
def article_embeddings(request, page_id):
    """
    API endpoint to fetch embedding visualization data for an article.

    Returns JSON with nodes array containing 2D coordinates.
    """
    from articles.models import ArticlePage

    try:
        page = Page.objects.get(pk=page_id).specific
    except Page.DoesNotExist:
        return JsonResponse({"error": "Page not found"}, status=404)

    if not isinstance(page, ArticlePage):
        return JsonResponse({"error": "Not an article page"}, status=400)

    if not page.live:
        return JsonResponse({"error": "Page not published"}, status=404)

    data = page.embedding_visualization or {"nodes": []}

    response = JsonResponse(data)
    response["Cache-Control"] = "public, max-age=3600"
    return response
