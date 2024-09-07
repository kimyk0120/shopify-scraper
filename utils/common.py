

def validate_url(url):
    if not url.startswith('https') or not url.startswith('http'):
        return 'https://' + url