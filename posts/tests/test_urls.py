from django.urls import reverse

from posts.lib.MyTestCase import MyTestCase


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
        for template, reverse_name \
                in PostsURLTests.templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class ProfileURLTests(MyTestCase):
    def test_profile_exists_at_desired_location(self):
        """Страница /<username>/
        доступна любому пользователю."""
        response = self.guest_client.get(
            reverse('posts:profile',
                    kwargs={'username': PostsURLTests.test_user.username})
        )
        self.assertEqual(response.status_code, 200)

    def test_current_post_exists_at_desired_location(self):
        """Страница /<username>/<post_id>/
        доступна любому пользователю."""
        response = self.guest_client.get(
            reverse('posts:post',
                    kwargs={'username': PostsURLTests.test_user.username,
                            'post_id': PostsURLTests.test_post.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_post_url_redirect_anonymous(self):
        """Страница /<username>/<post_id>/edit/
        перенаправляет анонимного пользователя."""
        response = self.guest_client.get(
            reverse('posts:post_edit',
                    kwargs={'username': PostsURLTests.test_user.username,
                            'post_id': PostsURLTests.test_post.id})
        )
        self.assertEqual(response.status_code, 302)

    def test_edit_post_url_redirect_non_author(self):
        """Страница /<username>/<post_id>/edit/
        перенаправляет НЕ автора."""
        response = self.non_author_client.get(
            reverse('posts:post_edit',
                    kwargs={'username': PostsURLTests.test_user.username,
                            'post_id': PostsURLTests.test_post.id})
        )
        self.assertEqual(response.status_code, 302)

    def test_edit_post_exists_at_desired_location_authorized(self):
        """Страница /<username>/<post_id>/edit/
        доступна для автора."""
        response = self.authorized_client.get(
            reverse('posts:post_edit',
                    kwargs={'username': PostsURLTests.test_user.username,
                            'post_id': PostsURLTests.test_post.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_post_page_uses_correct_template(self):
        """URL-адрес использует шаблон new_post.html."""
        response = self.authorized_client.get(
            reverse('posts:post_edit',
                    kwargs={'username': PostsURLTests.test_user.username,
                            'post_id': PostsURLTests.test_post.id})
        )
        self.assertTemplateUsed(response, 'new_post.html')

    def test_edit_post_page_non_author_redirect(self):
        """Правильный редирект НЕ автора при попытке отредактировать."""
        response = self.non_author_client.get(
            reverse('posts:post_edit',
                    kwargs={'username': PostsURLTests.test_user.username,
                            'post_id': PostsURLTests.test_post.id}),
            follow=True
        )
        self.assertRedirects(
            response,
            f'/{self.test_user.username}/{self.test_post.id}/'
        )
