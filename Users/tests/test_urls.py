from django.test import SimpleTestCase
from Users import views
from django.urls import reverse, resolve


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse('manage-profile')
        self.assertEquals(resolve(url).func, views.profile)

    def test_change_password_url_is_resolved(self):
        url = reverse('change-password')
        self.assertEquals(resolve(url).func, views.change_password)

    def test_edit_password_url_is_resolved(self):
        url = reverse('edit-profile')
        self.assertEquals(resolve(url).func, views.edit_profile)

    def test_favrioute_list_url_is_resolved(self):
        url = reverse('favrioute-list')
        self.assertEquals(resolve(url).func, views.favrioute_list)

    def test_orders_url_is_resolved(self):
        url = reverse('orders')
        self.assertEquals(resolve(url).func, views.my_orders)

    def test_cancel_book_url_is_resolved(self):
        url = reverse('cancel-book', args=[1])
        self.assertEquals(resolve(url).func, views.cancel_book)
