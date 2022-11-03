from django.shortcuts import render
from django.views import View
import tempfile
import pycodestyle
from io import StringIO
import sys

class Main(View):

    def get(self, request, *args, **kwargs):
        return render(request, "main.html", {"results": ""})
    
    def post(self, request, *args, **kwargs):

        with tempfile.TemporaryDirectory() as tmpdirname:

            with open(f"{tmpdirname}/code.py", "w") as file:
                file.write(request.POST["code"])
            
            style = pycodestyle.StyleGuide(show_source=False, quiet=False, \
                                           reporter=pycodestyle.StandardReport, offset=4)
            sys.stdout = buffer = StringIO()
            results = style.check_files([f"{tmpdirname}/code.py"])
            messages = buffer.getvalue().split("\n")
            sys.stdout = sys.__stdout__
            
            messages_list = []
            for message in messages:
                if len(message) > 0:
                    message = message.split(":")
                    line_number = message[1]
                    error = message[3]
                    messages_list.append(f"{line_number}: {error}")
            
        if len(messages_list) == 0:
            messages_list.append("All clear, no errors found")
        return render(request, "main.html", 
                      {"results": messages_list,
                       "content": request.POST["code"]})
