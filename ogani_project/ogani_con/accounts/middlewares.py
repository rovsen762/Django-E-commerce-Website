from django.contrib.auth import logout
from django.shortcuts import redirect


class RestrictAdminUserInFrontend():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.find("/admin/") == -1 and request.user.is_authenticated and request.user.is_superuser:
             logout(request)
             return redirect('login')
        response = self.get_response(request)
        return response