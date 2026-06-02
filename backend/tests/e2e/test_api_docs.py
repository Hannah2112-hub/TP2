import pytest
from seleniumbase import BaseCase

pytestmark = pytest.mark.e2e

class TestBackendDocs(BaseCase):
    def test_swagger_docs_load(self):
        self.open("http://127.0.0.1:8000/docs")
        self.assert_title_contains("Swagger UI")
        self.assert_element("h1.title")
        self.save_screenshot("swagger_docs_load")

    def test_navigation_to_redoc(self):
        self.open("http://127.0.0.1:8000/redoc")
        self.assert_title_contains("ReDoc")
        self.save_screenshot("redoc_load")
