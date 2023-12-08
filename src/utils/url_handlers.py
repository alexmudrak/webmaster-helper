from urllib.parse import urlparse, urlunparse


def get_correct_url(url_string: str) -> str:
    """
    Ensure a valid URL string and return it in a normalized form.
    """
    if not url_string.lower().startswith(("http://", "https://")):
        url_string = f"https://{url_string.lower()}"

    parsed_url = urlparse(url_string)

    if len(parsed_url.netloc.split(".")) < 2:
        raise ValueError("Invalid URL value.")

    url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            parsed_url.query,
            parsed_url.fragment,
        )
    )

    return url


def get_correct_domain(url_string: str) -> str:
    """
    Ensure a valid DOMAIN string and return it in a normalized form.
    """
    if not url_string.lower().startswith(("http://", "https://")):
        url_string = f"https://{url_string.lower()}"

    parsed_url = urlparse(url_string)

    if len(parsed_url.netloc.split(".")) < 2:
        raise ValueError("Invalid DOMAIN value.")

    url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            "",
            "",
            "",
            "",
        )
    )

    return url


def get_domain_from_url(url: str) -> str:
    url = get_correct_url(url)
    parsed_url = urlparse(url)
    return parsed_url.netloc
