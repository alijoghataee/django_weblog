from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from django.shortcuts import reverse


class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user sample')
        cls.post1 = Post.objects.create(
            title='post sample',
            text='text sample',
            status=Post.STATUS_CHOICES[0][0],
            author=cls.user,
        )
        cls.post2 = Post.objects.create(
            title='post sample2',
            text='text sample2',
            status=Post.STATUS_CHOICES[1][0],
            author=cls.user,
        )

    def test_post_model_str(self):
        post = self.post1
        self.assertEqual(str(post), post.title)

    def test_post_detail(self):
        post = self.post1
        self.assertEqual(post.title, self.post1.title)
        self.assertEqual(post.text, self.post1.text)

    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_title_on_blog_list_page(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)

    def test_post_detail_url(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_by_name(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)

    def test_post_details_on_blog_detail_page(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_status_404_if_post_id_not_exist(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id+99]))
        self.assertEqual(response.status_code, 404)

    def test_page_posts_list_use_template_base(self):
        response = self.client.get(reverse('posts_list'))
        self.assertTemplateUsed(response, '_base.html')

    def test_page_post_detail_use_template_base(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertTemplateUsed(response, '_base.html')

    def test_draft_post_not_show_in_posts(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_crete_view(self):
        response = self.client.post(reverse('add_post'), {
            'title': 'title create test',
            'text': 'text create test',
            'status': Post.STATUS_CHOICES[0][0],
            'author': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'title create test')

    def test_post_modify_view(self):
        response = self.client.post(reverse('modify_view', args=[self.post2.id]), {
            'title': 'title modify',
            'text': 'modify text',
            'status': Post.STATUS_CHOICES[0][0],
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'title modify')
        self.assertEqual(Post.objects.last().text, 'modify text')

    def test_delete_view(self):
        response = self.client.post(reverse('delete_post', args=[self.post1.id]), {
            'title': 'title',
            'text': 'text',
        })
        self.assertEqual(response.status_code, 302)
