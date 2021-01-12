from django.urls import reverse

from posts.models import Post
from posts.lib.MyTestCase import MyTestCase


class PostsFormTests(MyTestCase):
    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()

        form_data = {
            'text': 'Очень содержательный тестовый текст',
            'group': self.test_group.id,
        }

        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post(self):
        """После редактирования изменяется соответствующая запись в БД."""
        response = self.authorized_client.get(
            reverse('posts:post_edit',
                    kwargs={'username': PostsFormTests.test_user.username,
                            'post_id': PostsFormTests.test_post.id})
        )
        form_data = response.context['form'].initial
        form_data['text'] = 'Обновлённый текст'

        self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True)

        self.assertTrue(Post.objects.filter(
            text='Обновлённый текст').exists())
