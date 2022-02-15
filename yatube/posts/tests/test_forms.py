from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group

User = get_user_model()


class PostFormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый текст',
            slug='test-slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый заголовок',
            pub_date='12.02.2022',
        )

    def setUp(self):
        self.user = PostFormsTests.user
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post_create = reverse('posts:post_create')
        self.post_edit = reverse(
            'posts:post_edit',
            kwargs={'post_id': self.post.id}
        )
        self.post_profile = reverse(
            'posts:profile',
            kwargs={'username': self.user}
        )
        self.post_posts = reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.id}
        )

    def test_form_valid_creation(self):
        """Проверяем создается ли новый пост."""
        post_count = Post.objects.count()
        form_data = {
            'group': self.group.pk,
            'text': 'Тест',
        }
        response = self.authorized_client.post(
            self.post_create,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, self.post_profile)
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                group=self.group.pk,
                text='Тест'
            )
        )

    def test_form_valid_edit(self):
        """Проверяем сохраняется ли пост."""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Новый текст',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            self.post_edit,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, self.post_posts)
        self.assertEqual(response.context.get('post').text, 'Новый текст')
        self.assertEqual(Post.objects.count(), post_count)

    def test_form_no_auth_creation(self):
        """Проверяем создание поста неавторизованным пользователем."""
        post_count = Post.objects.count()
        response = f'/auth/login/?next={self.post_create}'
        self.assertRedirects(
            self.guest_client.get(self.post_create, follow=True),
            response
        )
        self.assertEqual(Post.objects.count(), post_count)
