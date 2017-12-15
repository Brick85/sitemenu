#from django.conf import settings
from sitemenu.sitemenu_settings import SERVER_CACHE_DIR, SERVER_CACHE_ARGS_FUNC
from sitemenu import import_item
import os
#import hashlib

from django.conf import settings
from django.utils import translation
from django.urls import reverse


class ForceAdminLanguageMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):
            request.LANGUAGE_CODE = getattr(settings, 'ADMIN_LANGUAGE_CODE', settings.LANGUAGE_CODE)
            translation.activate(request.LANGUAGE_CODE)
            request.LANG = request.LANGUAGE_CODE

        response = self.get_response(request)
        return response


class ForceDefaultLanguageMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']

        response = self.get_response(request)
        return response


class ServerCacheMiddleware(object):

    def _should_update_cache(self, request, response):
        if request.method != 'GET':
            return False

        if len(request.GET) > 0:
            return False

        if response.status_code != 200:
            return False

        return True

    def process_response(self, request, response):

        if not SERVER_CACHE_DIR or not hasattr(request, '_server_cache'):
            return response

        if 'argsfunc' in request._server_cache and request._server_cache['argsfunc']:
            func = request._server_cache['argsfunc']
        elif SERVER_CACHE_ARGS_FUNC:
            func = import_item(SERVER_CACHE_ARGS_FUNC)
        else:
            func = None

        if callable(func):
            strargs = func(request, response)
        else:
            strargs = ''

        if 'set_cookie' in request._server_cache:
            if strargs != '':
                response.set_cookie('scas', strargs, 60 * 60 * 24 * 360)
            else:
                response.delete_cookie('scas')
            return response

        if not self._should_update_cache(request, response):
            return response

        filename = "cache{0}.html".format(strargs)
        dirname = os.path.join(SERVER_CACHE_DIR, request.get_full_path()[1:])

        path_to_file = os.path.join(dirname, filename)

        try:
            os.makedirs(dirname)
        except OSError:
            pass

        f = open(path_to_file, 'w')
        f.write(response.content)
        f.close()
        return response
