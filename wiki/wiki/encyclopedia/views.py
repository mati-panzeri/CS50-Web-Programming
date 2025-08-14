from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from . import util
import random

class SearchForm(forms.Form):
    q = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Search Encyclopedia',
        'class': 'search'
        }))

class NewPageForm(forms.Form):
    title = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Enter Title',
        'class': 'form-control'
    }))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'placeholder': 'Enter Content',
        'class': 'textarea form-control',
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

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].strip()
            content = form.cleaned_data["content"].strip()
            if title and content:
                util.save_entry(title, content)
                return redirect(reverse("title", args=[title]))
            else:
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error": "Title and content cannot be empty."
                })
    else:
        form = NewPageForm()

    return render(request, "encyclopedia/new_page.html", {
        "form_new_entry": form
    })

def edit(request, title):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].strip()
            content = form.cleaned_data["content"].strip()
            if title and content:
                util.save_entry(title, content)
                return redirect(reverse("title", args=[title]))
    else:
        entry = util.get_entry(title)
        if not entry:
            return render(request, "encyclopedia/err.html")
        form = NewPageForm(initial={"title": title, "content": entry})
        form.fields["title"].widget.attrs['readonly'] = True
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "entry": entry,
            "form_edit_entry": form
    })

def random_page(request):
    entries = util.list_entries()
    if entries:
        title = random.choice(entries)
        return redirect(reverse("title", args=[title]))