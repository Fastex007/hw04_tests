from django.test import TestCase, Client

from posts.lib.MyTestCase import MyTestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_page_technologies(self):
        """Страница technologie/ ещё не создана"""
        response = self.guest_client.get('technologie/')
        self.assertEqual(response.status_code, 404)

    def test_page_about_author(self):
        """Страница about_author/ ещё не создана"""
        response = self.guest_client.get('about_author/')
        self.assertEqual(response.status_code, 404)


class PostsURLTests(MyTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.templates_url_names = {
            'index.html': '/',
            'group.html': '/group/test_group/',
            'new_post.html': '/new/',
        }

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_posts_url_exists_at_desired_location(self):
        """Страница /group/test_group/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test_group/')
        self.assertEqual(response.status_code, 200)

    def test_new_post_url_exists_at_desired_location_authorized(self):
        """Страница /new/ доступна только авторизованному пользователю."""
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_group_posts_url_redirect_anonymous(self):
        """Страница /new/ перенаправляет анонимного пользователя."""
        response = self.guest_client.get('/new/')
        self.assertEqual(response.status_code, 302)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for template, reverse_name in PostsURLTests.templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
