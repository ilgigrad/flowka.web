import re
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect

EXEMPT_URLS=[re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings,'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS+= [re.compile(url.lstrip('/')) for url in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        response = self.get_response(request)

        return response


    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request,'user')
        path=request.path_info.lstrip('/')
        is_exempt_url = any(url.match(path) for url in EXEMPT_URLS)
        if not request.user.is_authenticated and not is_exempt_url:
            return HttpResponseRedirect(settings.LOGIN_URL)
