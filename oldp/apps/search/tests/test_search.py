from django.test import LiveServerTestCase
from rest_framework.test import APIClient

from oldp.utils.test_utils import ElasticsearchTestMixin, real_es_test


class SearchAPITestCase(ElasticsearchTestMixin, LiveServerTestCase):
    """Test search API against real Elasticsearch."""

    fixtures = [
        "locations/countries.json",
        "locations/states.json",
        "locations/cities.json",
        "courts/courts.json",
        "cases/cases.json",
    ]

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.index_fixtures()

    @real_es_test
    def test_case_search_returns_results(self):
        """Test that searching cases returns results from ES."""
        response = self.client.get("/api/cases/search/", {"text": "test"})

        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIn("results", data)

    @real_es_test
    def test_case_search_without_text_returns_400(self):
        """Test that missing text parameter returns 400."""
        response = self.client.get("/api/cases/search/")

        self.assertEqual(400, response.status_code)
