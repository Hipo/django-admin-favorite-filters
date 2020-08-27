from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from django.http.response import Http404
from django.urls import reverse
from django_admin_favorite_filters.models import FavoriteFilter
from django_admin_favorite_filters.admin import FavoriteFilterAdmin


class FavoriteFilterTests(TestCase):

    def create_user(self):
        self.username = "test_admin"
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.user = user

    def setUp(self):
        site = AdminSite()
        self.admin = FavoriteFilterAdmin(FavoriteFilter, site)

        self.create_user()
        client = Client()
        client.login(username=self.username, password=self.password)
        self.client = client

    def add_filter(self):
        model = ContentType.objects.get_for_model(User)

        favorite_filter = FavoriteFilter(
            name="Staff Filter", filtered_model=model, query_parameters='is_staff=True')

        self.admin.save_model(obj=favorite_filter,
                              request=self.user, form=None, change=None)
        self.favorite_filter = favorite_filter

    def test_list(self):
        path = '/admin/django_admin_favorite_filters/favoritefilter/'

        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        self.add_filter()

        path = f"/admin/django_admin_favorite_filters/favoritefilter/{self.favorite_filter.id}/change/"
        response = self.client.post(path)
        self.assertEqual(response.status_code, 200)

    def test_add_favorite_filter(self):
        add_favorite_url = reverse('admin:%s_%s_add' % (
            FavoriteFilter._meta.app_label, FavoriteFilter._meta.model_name))

        filtered_model = ContentType.objects.get_for_model(User)
        add_favorite_url = f"{add_favorite_url}?filtered_model={filtered_model.id}&query_parameters='is_active=True'"

        response = self.client.post(add_favorite_url)
        self.assertEqual(response.status_code, 200)

    def test_delete_model(self):
        self.add_filter()

        filter_to_delete = get_object_or_404(
            FavoriteFilter, id=self.favorite_filter.id)

        self.admin.delete_model(self.user, filter_to_delete)
        with self.assertRaises(Http404):
            deleted = get_object_or_404(
                FavoriteFilter, id=self.favorite_filter.id)
