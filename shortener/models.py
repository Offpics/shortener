from django.db import models
from .validators import CustomURLValidator


class Short(models.Model):
    """ Table that stores original URLs and short URLs. """

    # Custom validator to allow only urls with no schemes.
    validator = CustomURLValidator(schemes=[''])

    # CharField for original URL.
    url = models.CharField(max_length=255, unique=True, validators=[validator])

    # CharField for short url.
    short = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return f'URL: {self.url}, short: {self.short}'
