from django.http import HttpRequest, HttpResponse


def get_robots_txt(request: HttpRequest) -> HttpResponse:
    """Returns special content to stop bots from crawling my site."""
    content = """
        User-agent: SemrushBot
        Disallow: /
        User-agent: SiteAuditBot
        Disallow: /
        User-agent: SemrushBot-BA
        Disallow: /
        User-agent: SemrushBot-SI
        Disallow: /
        User-agent: SemrushBot-SWA
        Disallow: /
        User-agent: SemrushBot-CT
        Disallow: /
        User-agent: SplitSignalBot
        Disallow: /
        User-agent: SemrushBot-COUB
        Disallow: /
    """.replace("        ", "").strip()
    return HttpResponse(content, content_type="text/plain")
