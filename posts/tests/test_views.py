from django.urls import reverse
from django import forms

from posts.lib.MyTestCase import MyTestCase
from posts.models import Post
from posts.views import POSTS_PER_PAGE


class PostsPagesTests(MyTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.templates_pages_names = {
            'index.html': reverse('index'),
            'group.html': (
                reverse('group', kwargs={'slug': 'test_group'})
            ),
            'new_post.html': reverse('new_post'),
        }

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for template, reverse_name in \
                PostsPagesTests.templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_index_context(self, response):
        """Проверяем контекст index.

        Вынесено в отдельную функцию чтобы не дублировать код
        """
        post_text_0 = response.context.get('page')[0].text
        post_author_0 = response.context.get('page')[0].author
        post_group_0 = response.context.get('page')[0].group

        self.assertEqual(post_text_0, PostsPagesTests.test_post.text)
        self.assertEqual(post_author_0, PostsPagesTests.test_user)
        self.assertEqual(post_group_0, PostsPagesTests.test_group)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('index'))

        self.check_index_context(response)

    def test_group_pages_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'test_group'})
        )
        self.assertEqual(response.context.get('group').title,
                         'Тестовая группа')
        self.assertEqual(response.context.get('group').slug, 'test_group')
        # Провряем на месте ли оказался новый пост
        self.check_index_context(response)

    def test_new_post_page_show_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(MyTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for i in range(12):
            Post.objects.create(
                group=cls.test_group,
                text=f'Тестовый текст {i}',
                author=cls.test_user,
            )

    def test_first_page_contains_ten_records(self):
        """Проверяем работу пагинации на главной страницу.

        Должно быть 10 записей
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list),
                         POSTS_PER_PAGE)

    def test_first_page_posts_contains(self):
        """Проверяем правильные ли записи выводятся на главную страницу.

        На первой странице пагинации
        """
        response = self.client.get(reverse('index'))
        for i in range(POSTS_PER_PAGE-1, 0):
            self.assertEqual(response.context.get('page').object_list[i].text,
                             f'Тестовый текст {i}')

    def test_second_page_contains_three_records(self):
        """Проверяем количество записей на второй странице пагинации.

        Должно быть 3 записи
        """
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)


class ProfileTests(MyTestCase):
    def test_edit_correct_form_fields(self):
        """Шаблон /edit/ сформирован с правильными полями."""
        response = self.authorized_client.get(
            reverse('post_edit',
                    kwargs={'username': ProfileTests.test_user.username,
                            'post_id': ProfileTests.test_post.id})
        )

        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_correct_context(self):
        """Шаблон /edit/ сформирован с правильными контекстом."""
        response = self.authorized_client.get(
            reverse('post_edit',
                    kwargs={'username': ProfileTests.test_user.username,
                            'post_id': ProfileTests.test_post.id})
        )

        form = response.context['form']
        from_data = form.initial

        self.assertEqual(from_data['text'], ProfileTests.test_post.text)
        self.assertEqual(from_data['group'], ProfileTests.test_group.id)

    def test_profile_correct_context(self):
        """Шаблон /<username>/ сформирован с правильными контекстом."""
        response = self.authorized_client.get(
            reverse('profile',
                    kwargs={'username': ProfileTests.test_user.username})
        )

        post_text_0 = response.context.get('page')[0].text
        post_author_0 = response.context.get('page')[0].author
        post_group_0 = response.context.get('page')[0].group

        self.assertEqual(post_text_0, ProfileTests.test_post.text)
        self.assertEqual(post_author_0, ProfileTests.test_user)
        self.assertEqual(post_group_0, ProfileTests.test_group)

    def test_one_post_correct_context(self):
        """Шаблон /<username>/<post_id>/.

        Сформирован с правильным контекстом
        """
        response = self.authorized_client.get(
            reverse('post',
                    kwargs={'username': ProfileTests.test_user.username,
                            'post_id': ProfileTests.test_post.id})
        )

        self.assertEqual(response.context.get('post').group,
                         ProfileTests.test_group)
        self.assertEqual(response.context.get('post').author.username,
                         ProfileTests.test_user.username)
        self.assertEqual(response.context.get('post').text,
                         ProfileTests.test_post.text)
