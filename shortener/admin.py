from django.contrib import admin
from .models import Short


# Define the admin class.
class ShortAdmin(admin.ModelAdmin):
    """ Create list view of the Short model as readonly. """
    list_display = ('url', 'short')
    readonly_fields = ('url', 'short')


# Register the ShortAdmin class with the Short model.
admin.site.register(Short, ShortAdmin)
