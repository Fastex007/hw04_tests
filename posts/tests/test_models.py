from posts.lib.MyTestCase import MyTestCase


class PostModelTest(MyTestCase):
    def test_verbose_name_post(self):
        """verbose_name в полях совпадает с ожидаемым. Модель Post"""
        post = PostModelTest.test_post
        field_verboses = {
            'text': 'Текст',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_verbose_name_group(self):
        """verbose_name в полях совпадает с ожидаемым. Модель Group"""
        group = PostModelTest.test_group
        field_verboses = {
            'title': 'Название',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

    def test_help_text_post(self):
        """help_text в полях совпадает с ожидаемым. Модель Post"""
        post = PostModelTest.test_post
        field_help_texts = {
            'text': 'Текст публикации',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)

    def test_help_text_group(self):
        """help_text в полях совпадает с ожидаемым. Модель Group"""
        group = PostModelTest.test_group
        field_help_texts = {
            'title': 'Группа, в которой может быть опубликован текст',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected)

    def test_str_post(self):
        """Проверяем, правильно ли работает метод __str__ модели Post"""
        post = PostModelTest.test_post
        str_value = post.text[:15]
        self.assertEquals(str_value, 'Тестовый текст,')

    def test_str_group(self):
        """Проверяем, правильно ли работает метод __str__ модели Group"""
        group = PostModelTest.test_group
        str_value = group.title
        self.assertEquals(str_value, 'Тестовая группа')
