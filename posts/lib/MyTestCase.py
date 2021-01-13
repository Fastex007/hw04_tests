import shutil
import tempfile

from django.conf import settings
from django.test import Client, TestCase

from posts.models import Group, Post, User


class MyTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

        cls.test_user = User.objects.create_user(
            username='test_user',
            password='123456'
        )

        cls.non_author = User.objects.create_user(
            username='non_author',
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
        self.non_author_client = Client()
        self.non_author_client.force_login(self.non_author)
