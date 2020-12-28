from django.urls import reverse

from posts.models import Post
from posts.lib.MyTestCase import MyTestCase


class PostsCreateFormTests(MyTestCase):
    def test_create_post(self):
        """Валидная форма создает запись в Task."""
        posts_count = Post.objects.count()

        form_data = {
            'text': 'Очень содержательный тестовый текст',
            'group': self.test_group.id,
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, '/')
        self.assertEqual(Post.objects.count(), posts_count + 1)

