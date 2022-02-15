from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост для проверки 15 символов',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post_task = self.post.__str__()
        group_task = self.group.__str__()
        task_list = {
            post_task: self.post.text[:15],
            group_task: self.group.title
        }
        for task, value in task_list.items():
            with self.subTest(task=task):
                self.assertEqual(task, value)

    def test_models_verbose_and_help(self):
        """
        Проверяем, что у моделей корректно работают verbose_name и help_text
        """
        post_verbose = self.post._meta.get_field('group').verbose_name
        post_help = self.post._meta.get_field('group').help_text
        task_list = {
            post_verbose: 'Группа',
            post_help: 'Группа, к которой будет относиться пост',
        }
        for task, value in task_list.items():
            with self.subTest(task=task):
                self.assertEqual(task, value)
