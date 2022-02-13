from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group
from posts.forms import PostForm

User = get_user_model()


class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый текст',
            slug='test-slug'
        )
        cls.other_group = Group.objects.create(
            title='Тестовый заголовок 2',
            description='Тестовый текст 2',
            slug='test_2-slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый заголовок',
            pub_date='12.02.2022',
        )

    def setUp(self):
        self.user = PostViewsTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post_index = reverse('posts:index')
        self.post_group = reverse(
            'posts:group_list',
            kwargs={'slug': f'{self.group.slug}'}
        )
        self.post_other_group = reverse(
            'posts:group_list',
            kwargs={'slug': f'{self.other_group.slug}'}
        )
        self.post_profile = reverse(
            'posts:profile',
            kwargs={'username': f'{self.user}'}
        )
        self.post_posts = reverse(
            'posts:post_detail',
            kwargs={'post_id': f'{self.post.id}'}
        )
        self.post_create = reverse('posts:post_create')
        self.post_edit = reverse(
            'posts:post_edit',
            kwargs={'post_id': f'{self.post.id}'}
        )

    def test_views_correct_template(self):
        """Проверяем соответствие view-функций адресам"""
        templates_names = {
            self.post_index: 'posts/index.html',
            self.post_group: 'posts/group_list.html',
            self.post_profile: 'posts/profile.html',
            self.post_posts: 'posts/post_detail.html',
            self.post_create: 'posts/create_post.html',
            self.post_edit: 'posts/create_post.html',
        }
        for address, template in templates_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_views_correct_context_index(self):
        """Проверяем соответствие контекста index"""
        response = self.authorized_client.get(self.post_index)
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object, self.post)

    def test_views_correct_context_group_list(self):
        """Проверяем соответствие контекста group_list"""
        response = self.authorized_client.get(self.post_group)
        first_object = response.context['page_obj'][0]
        second_object = first_object.group
        self.assertEqual(first_object, self.post)
        self.assertEqual(second_object, self.group)

    def test_views_correct_context_profile(self):
        """Проверяем соответствие контекста profile"""
        response = self.authorized_client.get(self.post_group)
        first_object = response.context['page_obj'][0]
        second_object = first_object.author
        self.assertEqual(first_object, self.post)
        self.assertEqual(second_object, self.post.author)

    def test_views_correct_context_post_detail(self):
        """Проверяем соответствие контекста post_detail"""
        response = self.authorized_client.get(self.post_posts)
        first_object = response.context['post']
        second_object = response.context.get('post').pk
        self.assertEqual(first_object, self.post)
        self.assertEqual(second_object, self.post.pk)

    def test_views_correct_context_post_edit(self):
        """Проверяем соответствие контекста post_edit"""
        response = self.authorized_client.get(self.post_edit)
        first_object = response.context['form']
        second_object = response.context['post_id']
        third_object = response.context['is_edit']
        self.assertIsInstance(first_object, PostForm)
        self.assertEqual(second_object, self.post.pk)
        self.assertTrue(third_object)

    def test_views_correct_context_post_create(self):
        """Проверяем соответствие контекста post_create"""
        response = self.authorized_client.get(self.post_create)
        first_object = response.context['form']
        second_object = response.context.get('is_edit', None)
        self.assertIsInstance(first_object, PostForm)
        self.assertIsNone(second_object)

    def test_views_correct_post_creation(self):
        """Проверяем что пост не попадает на страницу другой группы"""
        response = self.authorized_client.get(self.post_other_group)
        first_object = len(response.context['page_obj'])
        self.assertEqual(first_object, 0)


class PaginatorViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.other_user = User.objects.create_user(username='NoName')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый текст',
            slug='test-slug'
        )
        cls.other_group = Group.objects.create(
            title='Тестовый заголовок 2',
            description='Тестовый текст 2',
            slug='test_2-slug'
        )
        cls.post_1 = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый заголовок 1',
            pub_date='12.02.2022',
        )
        cls.post_2 = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый заголовок 2',
            pub_date='13.02.2022',
        )
        cls.post_3 = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый заголовок 3',
            pub_date='14.02.2022',
        )
        cls.post_4 = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый заголовок 4',
            pub_date='15.02.2022',
        )
        cls.post_5 = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый заголовок 5',
            pub_date='16.02.2022',
        )
        cls.post_6 = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый заголовок 6',
            pub_date='17.02.2022',
        )
        cls.post_7 = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый заголовок 7',
            pub_date='18.02.2022',
        )
        cls.post_8 = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый заголовок 8',
            pub_date='19.02.2022',
        )
        cls.post_9 = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый заголовок 9',
            pub_date='20.02.2022',
        )
        cls.post_10 = Post.objects.create(
            author=cls.user,
            group=cls.other_group,
            text='Тестовый заголовок 10',
            pub_date='21.02.2022',
        )
        cls.post_11 = Post.objects.create(
            author=cls.other_user,
            group=cls.group,
            text='Тестовый заголовок 11',
            pub_date='22.02.2022',
        )
        cls.post_12 = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый заголовок 12',
            pub_date='23.02.2022',
        )
        cls.post_13 = Post.objects.create(
            author=cls.user,
            group=cls.other_group,
            text='Тестовый заголовок 13',
            pub_date='24.02.2022',
        )

    def setUp(self):
        self.user = PaginatorViewsTests.user
        self.other_user = PaginatorViewsTests.other_user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.other_client = Client()
        self.other_client.force_login(self.other_user)
        self.post_index = reverse('posts:index')
        self.post_group = reverse(
            'posts:group_list',
            kwargs={'slug': f'{self.group.slug}'}
        )
        self.post_profile = reverse(
            'posts:profile',
            kwargs={'username': f'{self.user}'}
        )

    def test_views_paginator_first_page(self):
        """Проверяем работу пажинатора, первая страница"""
        paths = {
            self.post_index,
            self.post_group,
            self.post_profile,
        }
        for path in paths:
            with self.subTest(path=path):
                response = self.authorized_client.get(path)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_views_paginator_second_page(self):
        """Проверяем работу пажинатора, вторая страница"""
        paths = {
            self.post_index: 3,
            self.post_group: 1,
            self.post_profile: 2,
        }
        for path, value in paths.items():
            with self.subTest(path=path):
                response = self.authorized_client.get(path + '?page=2')
                self.assertEqual(len(response.context['page_obj']), value)
