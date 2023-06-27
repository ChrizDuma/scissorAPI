import unittest
from flask import Flask
from flask_restx import Api
from ..routes.url import short_namespace
from ..models import Link


class ShortUrlTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.api = Api(cls.app)
        cls.api.add_namespace(short_namespace)
        cls.client = cls.app.test_client()

    def test_shorten_url(self):
        url = "http://example.com"

        response = self.client.post("/short/short_url", json={"original_url": url})

        self.assertEqual(response.status_code, 201)
        self.assertIn("short_url", response.json)

    def test_shorten_url_invalid_url(self):
        url = "example.com"  # Invalid URL

        response = self.client.post("/short/short_url", json={"original_url": url})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["message"], "Invalid url")

    def test_shorten_url_existing_url(self):
        url = "http://example.com"

        # Add the URL to the database
        link = Link(user_id=1, original_url=url)
        link.save()

        response = self.client.post("/short/short_url", json={"original_url": url})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["message"], "Url already exists")

    def test_redirect_short_url(self):
        url = "http://example.com"

        # Add the URL to the database
        link = Link(user_id=1, original_url=url)
        link.save()

        response = self.client.get(f"/short/{link.short_url}")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], url)

    def test_redirect_short_url_not_found(self):
        short_url = "abc123"  # Non-existent short URL

        response = self.client.get(f"/short/{short_url}")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Url not found")


# if __name__ == "__main__":
#     unittest.main()
