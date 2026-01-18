from django.shortcuts import redirect
from django.urls import reverse
class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            path_to_redirect = [reverse('login'),reverse('register')]

            if request.path in path_to_redirect:
                return redirect(reverse('index'))
            
        response = self.get_response(request)
        return response

class RestrictUnauthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = [reverse('dashboard')]

        if not request.user.is_authenticated and request.path in restricted_paths:
            return redirect(reverse('login'))
        
        response = self.get_response(request)
        return response