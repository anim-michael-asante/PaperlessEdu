from django.test import SimpleTestCase
from django.urls import reverse


class WelcomePageTests(SimpleTestCase):
    def test_welcome_page_status_and_template(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/welcome.html')

    def test_favicon_links_present(self):
        response = self.client.get(reverse('welcome'))
        content = response.content.decode('utf-8')
        self.assertIn('static/core/favicon.ico', content)
        self.assertIn('static/core/favicon-32x32.png', content)
        self.assertIn('static/core/apple-touch-icon.png', content)
        self.assertIn('static/core/site.webmanifest', content)

    def test_social_share_open_graph_meta_tags(self):
        response = self.client.get(reverse('welcome'))
        content = response.content.decode('utf-8')
        self.assertIn('property="og:image"', content)
        self.assertIn('static/core/og-image.png', content)
        self.assertIn('name="twitter:card" content="summary_large_image"', content)
        self.assertIn('name="twitter:image"', content)

    def test_brand_logo_and_emblem_in_page(self):
        response = self.client.get(reverse('welcome'))
        content = response.content.decode('utf-8')
        self.assertIn('static/core/paperlessedu-icon.png', content)
        self.assertIn('static/core/paperlessedu-logo.png', content)
