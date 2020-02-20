import re

def urlify_username(url):
    url = re.sub(r"[^\w\s]", '', url)
    url = re.sub(r"\s+", '', url)
    return url

def urlify_title(url):
    url = re.sub(r"[^\w\s]", '', url)
    url = re.sub(r"\s+", '_', url)
    return url