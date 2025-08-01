from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    entry = util.get_entry(title)

    if entry:
            return render(request, f"encyclopedia/entry.html", {
                "title": title.capitalize(),
                "entry": entry
            })
    else:
        return render (request, "encyclopedia/err.html")