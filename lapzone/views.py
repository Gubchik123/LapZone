from django.http import HttpRequest, HttpResponse


def get_robots_txt(request: HttpRequest) -> HttpResponse:
    """Returns special content to stop bots from crawling my site."""
    return HttpResponse(
        "User-agent: SemrushBot\nDisallow: /", content_type="text/plain"
    )
