from django.http import HttpResponseForbidden
from .permissions import is_admin_global, is_admin_grupo

def admin_grupo_ou_global(view_func):
    def wrapper(request, *args, **kwargs):
        if is_admin_global(request.user) or is_admin_grupo(request.user):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Acesso negado")
    return wrapper
