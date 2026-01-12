from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.models import User

class SetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.setup_complete = User.objects.filter(is_superuser=True).exists()

    def __call__(self, request):
        if self.setup_complete:
            return self.get_response(request)
        try:
            setup_url = reverse('setup')
            admin_prefix = reverse('admin:index')
        except NoReverseMatch:

            return self.get_response(request)

        if request.path_info.startswith(admin_prefix) or request.path_info == setup_url:
            return self.get_response(request)


        return redirect(setup_url)

