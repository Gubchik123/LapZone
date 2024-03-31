from django.http import HttpRequest, HttpResponse


def get_robots_txt(request: HttpRequest) -> HttpResponse:
    """Returns special content to stop bots from crawling my site."""
    content = """
        User-agent: *
        Disallow: /
    """.replace("        ", "").strip()
    return HttpResponse(content, content_type="text/plain")
