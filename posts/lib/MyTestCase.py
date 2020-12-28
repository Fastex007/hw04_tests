from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group


class MyTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.test_user = get_user_model().objects.create_user(
            username='test_user',
            password='123456'
        )

        cls.test_group = Group.objects.create(
            id=1,
            title='Тестовая группа',
            slug='test_group',
        )

        cls.test_post = Post.objects.create(
            id=1,
            group=cls.test_group,
            text='Тестовый текст, который надо чтобы был длиннее пятнадцати '
                 'символов, а то ничего не получится. '
                 'один два три четрые пять',
            author=cls.test_user,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.test_user)