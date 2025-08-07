from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from . import util

class SearchForm(forms.Form):
    q = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Search Encyclopedia',
        'class': 'search'
        }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
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

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["q"].strip().lower()
            # Search for exact match first
            entries = util.list_entries()
            for entry in entries:
                if entry.lower() == query:
                    return redirect(reverse("title", args=[entry]))
            # Search for partial matches
            results = [e for e in entries if query in e.lower()]
            return render(request, "encyclopedia/search_results.html", {
                "query": form.cleaned_data["q"],
                "entries": results,
                "form": SearchForm()
            })