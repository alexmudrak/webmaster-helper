import pytest

from utils.url_handlers import (
    get_correct_domain,
    get_correct_url,
    get_domain_from_url,
)


class TestUrlHandler:
    def test_get_correct_url_valid_url(self):
        result = get_correct_url("http://example.com")
        assert result == "http://example.com"

    def test_get_correct_url_valid_url_https(self):
        result = get_correct_url("https://example.com")
        assert result == "https://example.com"

    def test_get_correct_url_normalize_url(self):
        result = get_correct_url("example.com")
        assert result == "https://example.com"

    def test_get_correct_url_invalid_url(self):
        with pytest.raises(ValueError, match="Invalid URL value."):
            get_correct_url("not_a_valid_url")

    def test_get_correct_domain_valid_url(self):
        result = get_correct_domain("http://example.com")
        assert result == "http://example.com"

    def test_get_correct_domain_normalize_url(self):
        result = get_correct_domain("example.com")
        assert result == "https://example.com"

    def test_get_correct_domain_invalid_url(self):
        with pytest.raises(ValueError, match="Invalid DOMAIN value."):
            get_correct_domain("not_a_valid_domain")

    def test_get_domain_from_url_valid_url(self):
        result = get_domain_from_url("http://example.com")
        assert result == "example.com"

    def test_get_domain_from_url_normalize_url(self):
        result = get_domain_from_url("example.com")
        assert result == "example.com"

    def test_get_domain_from_url_invalid_url(self):
        with pytest.raises(ValueError, match="Invalid URL value."):
            get_domain_from_url("not_a_valid_url")
