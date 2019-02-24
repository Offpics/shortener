from django.core.validators import URLValidator


class CustomURLValidator(URLValidator):
    """ Custom URLValidator that allows to use empty scheme ''. """

    def __call__(self, value):
        if '://' not in value:
            value = 'http://' + value
        super(CustomURLValidator, self).__call__(value)
