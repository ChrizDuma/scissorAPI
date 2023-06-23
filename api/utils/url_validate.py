import requests
from urllib.error import URLError


def validate_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        response = requests.head(url)
        return response.ok
    except (requests.RequestException, URLError):
        return False

