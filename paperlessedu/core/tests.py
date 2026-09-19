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

    def test_navigation_tabs_present(self):
        response = self.client.get(reverse('welcome'))
        content = response.content.decode('utf-8')
        self.assertIn('href="#how-it-works"', content)
        self.assertIn('href="#services"', content)
        self.assertIn('href="#what-you-get"', content)
        self.assertIn('href="#testimonials"', content)
        self.assertIn('href="#faq"', content)
        self.assertIn('Services', content)
        self.assertIn("What You'll Get", content)
        self.assertIn('Testimonials', content)
        self.assertIn('FAQ', content)

    def test_new_sections_rendered(self):
        response = self.client.get(reverse('welcome'))
        content = response.content.decode('utf-8')
        self.assertIn('id="services"', content)
        self.assertIn('id="what-you-get"', content)
        self.assertIn('id="testimonials"', content)
        self.assertIn('id="faq"', content)
        self.assertIn('class="faq-item"', content)

    def test_reference_contact_card_rendered(self):
        response = self.client.get(reverse('welcome'))
        content = response.content.decode('utf-8')
        self.assertIn('class="contact-card"', content)
        self.assertIn('class="contact-light-bloom"', content)
        self.assertIn('class="contact-card-badge"', content)
        self.assertIn('School Onboarding &amp; Setup', content)
        self.assertIn('Ready to transform your school?', content)
        self.assertIn('button--contact-primary', content)
        self.assertIn('button--contact-glass', content)
        self.assertIn('href="mailto:hello@paperlessedu.com"', content)
        self.assertIn('href="#how-it-works"', content)

    def test_inspiration_matched_footer_rendered(self):
        response = self.client.get(reverse('welcome'))
        content = response.content.decode('utf-8')
        self.assertIn('class="footer-grid"', content)
        self.assertIn('class="footer-col footer-col--brand"', content)
        self.assertIn('Built by Aerixis', content)
        self.assertIn('Platform', content)
        self.assertIn('Core Modules', content)
        self.assertIn('Stay Updated', content)
        self.assertIn('class="newsletter-form"', content)
        self.assertIn('class="newsletter-input"', content)
        self.assertIn('class="newsletter-submit-btn"', content)
        self.assertIn('class="footer-bottom-bar"', content)
