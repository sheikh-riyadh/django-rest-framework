from django.shortcuts import redirect
from django.views import View

class ApiRoot(View):
    def get(self, request):
        return redirect('api-root')