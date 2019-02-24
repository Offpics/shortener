from hashlib import md5

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError
from .forms import ShortenerForm
from .models import Short


def index(request):
    """ Index page for the application.

    Index page contains Form with one input of URL to shorten.
    GET method returns empty ShortenerForm with one input of URL to shorten.

    POST method tries to return short URL of the given URL.
    If the URL exists in the database, this function returns short URL.
    If the URL does not exist in the database, generate short URL,
    save it to the database and return it to the user.
    Short URL is generated by calculating the MD5 hash of the URL and trying
    to extract a given number of characters from it.
    If the calculated hash is not suitable for the link, generate
    a new hash with salt and try to use it.
    """
    if request.method == 'POST':
        form = ShortenerForm(request.POST)
        if form.is_valid():
            # Get clean URL from the form.
            url = form.cleaned_data.get('url')

            # Remove any unnecessary parts from the URL
            # to avoid repetiton in the database.
            url = url.replace('http://', '')
            url = url.replace('https://', '')
            url = url.replace('www.', '')

            # Check wheter URL already exists in the database.
            # If it exists return early without calculating the short.
            try:
                # Check wheter URL already exists in the database.
                short = Short.objects.get(url=url)
            except Short.DoesNotExist:
                # Object does not exist in the database so pass
                # and calcualte the short.
                pass
            else:
                # Return early with short URL.
                messages.success(request, f'{short.short}')
                return redirect('index')

            # Lenght of short URL.
            short_len = 7

            # Salt in collision case.
            salt = '1'

            # Calculate md5 hash of the url.
            short = md5(bytes(url, encoding='utf-8')).hexdigest()

            # Try to find suitable short URL and save it to database.
            while True:
                # Iterate over the hash and try to create short URL.
                for i in range(0, len(short)-short_len, short_len):
                    short_tmp = short[i:i+short_len]
                    try:
                        Short.objects.create(url=url, short=short_tmp)
                    except IntegrityError:
                        # Short already exists in the database.
                        # Skip the iteration.
                        continue
                    else:
                        # We created the object succesfully
                        # so return early.
                        messages.success(request, f'{short_tmp}')
                        return redirect('index')

                # If we didn't find suitable short, calculate new hash
                # with a salt.
                short = md5(bytes(url+salt, encoding='utf-8')).hexdigest()

                # Increment salt for the next possible iteration.
                salt += 1

    else:
        # Empty form.
        form = ShortenerForm()

    return render(request, 'shortener/index.html', {'form': form})


def short(request, short):
    """ Function to handle redirecting to other sites.

    If given short URL is in the database, redirect user to the original URL.
    Otherwise, display a warning message that given short URL does not exist.
    """

    try:
        # Get object of given short URL.
        data = Short.objects.get(short=short)

        # Get original URL of the short.
        redirect_url = data.url

        # Redirect user to the original URL.
        return redirect(f'http://{redirect_url}')
    except Short.DoesNotExist:
        # Display warning to the user and redirect to index page.
        messages.warning(request, f'Short URL: {short} does not exist.')
        return redirect('index')
