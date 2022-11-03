from django.shortcuts import render
from django.views import View

class Main(View):

    def get(self, request, *args, **kwargs):
        return render(request, "main.html")
    
    def post(self, request, *args, **kwargs):
        pass
