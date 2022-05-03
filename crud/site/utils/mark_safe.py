from django.utils import safestring


def mark_safe(str_url: str, data, replace='replace'):
    url = str_url.replace(replace, str(data))
    return safestring.mark_safe(url)
