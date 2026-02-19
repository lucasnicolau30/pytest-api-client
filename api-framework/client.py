import requests
import time
from .config import get_base_url
from .utils import build_url


class APIClient:
    def __init__(self, base_url = None, headers = None, timeout = 10):
        self.base_url = base_url or get_base_url()
        self.session = requests.Session()
        self.timeout = timeout

        if headers:
            self.session.headers.update(headers)

    def get(self, endpoint, **kwargs):
        """Perform a GET request and attach custom response timing."""
        url = build_url(self.base_url, endpoint)

        start = time.perf_counter()
        response = self.session.get(url, timeout = self.timeout, **kwargs)
        end = time.perf_counter()

        # custom timing for performance tests
        response.elapsed_custom = end - start
        return response

    def close(self):
        """Close the HTTP session."""
        self.session.close()
