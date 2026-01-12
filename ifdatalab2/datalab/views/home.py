from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def home_redirect(request):
    grupo_id = request.session.get("grupo_id")
    if grupo_id:
        return redirect("dashboard_grupo", grupo_id=grupo_id)
    else:
        return redirect("selecionar_grupo")