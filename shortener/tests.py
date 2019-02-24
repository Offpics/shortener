from django.test import TestCase
from .models import Short
from .forms import ShortenerForm
from django.db.utils import IntegrityError


class ShortTestCase(TestCase):
    """ Test case for Short table in the database. """

    def test_unique_url(self):
        """ Test unique constraint on url field."""
        Short.objects.create(url='example.com/', short='123456')
        with self.assertRaises(IntegrityError):
            Short.objects.create(url='example.com/', short='111111')

    def test_unique_short(self):
        """ Test unique constraint on short field."""
        Short.objects.create(url='example.com/', short='123456')
        with self.assertRaises(IntegrityError):
            Short.objects.create(url='example2.com/', short='123456')

    def test_unique_both(self):
        """ Test unique constraints on url and short fields."""
        Short.objects.create(url='example.com/', short='123456')
        with self.assertRaises(IntegrityError):
            Short.objects.create(url='example.com/', short='123456')


class ShortenerFormTestCase(TestCase):
    """ Test case for ShortenerForm form."""

    def test_invalid_url(self):
        """ Test form validation with invalid urls."""

        form_data = {'url': 'ftp://example.com'}
        form = ShortenerForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'url': 'ftps://example.com'}
        form = ShortenerForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'url': 'invalid.m'}
        form = ShortenerForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_url(self):
        """ Test form validation with valid urls."""

        form_data = {'url': 'example.com'}
        form = ShortenerForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'url': 'https://example.com'}
        form = ShortenerForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'url': 'http://example.pl'}
        form = ShortenerForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'url': 'bit.ly'}
        form = ShortenerForm(data=form_data)
        self.assertTrue(form.is_valid())
