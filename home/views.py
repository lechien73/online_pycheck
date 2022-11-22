from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import tempfile
import pycodestyle
import requests
from io import StringIO
import sys


class Main(View):
    """
    The get request simply renders the editor
    The post request runs pycodestyle in a temporary directory
    """

    def get(self, request, *args, **kwargs):
        """
        As simple a view as it's possible to get
        """
        return render(request, "main.html")

    def post(self, request, *args, **kwargs):
        """
        Hmmm...some weirdness here!
        1. Get the contents of the editor
        2. Create a temporary directory and write it there
        3. Divert the stdout to a buffer
        4. Run pycodestyle against the file
        5. Put stdout back to normal

        Why the stdout hack?? Seems a bit hacky, Matt!
        Because I could not figure out how to get pycodestyle
        to give me line numbers in any of the reporters. So,
        I take what is spat out to stdout and mangle it.
        Clear?
        """

        with tempfile.TemporaryDirectory() as tmpdirname:

            with open(f"{tmpdirname}/code.py", "w") as file:
                file.write(request.POST["code"])

            style = pycodestyle.StyleGuide(show_source=False, quiet=False,
                                           reporter=pycodestyle.StandardReport,
                                           offset=4)
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
                    msg = f"<a href='#' onclick='goto({line_number})'>"
                    msg += f"{line_number}</a>: {error}<br>"
                    messages_list.append(msg)

        if len(messages_list) == 0:
            messages_list.append("All clear, no errors found")
        return HttpResponse(messages_list)


class Api(View):

    def get(self, request, url, *args, **kwargs):

        if url[0:5] == "https":
            url = url.split("https://")
            if url[1][-3:] != ".py":
                content = "# *** ERROR ***\n"
                content += "# Must be a Python file!\n"
                content += "# Extension is not .py\n"
            else:
                response = requests.get("https://" + url[1])
                if response.status_code == 200:
                    content = response.content.decode("utf-8")
                else:
                    content = "# *** ERROR ***\n"
                    content += "# Error loading the Python file\n"
                    content += f"# Status code: {response.status_code}\n"
        else:
            content = "# *** ERROR ***\n"
            content += "# Python file could not be loaded\n# URL scheme "
            content += f"must be https://\n# You supplied: {url}\n"

        return render(request, "main.html", context={"content": content})
