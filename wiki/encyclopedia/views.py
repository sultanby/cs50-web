from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from random import randint

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Name of title", widget=forms.TextInput(attrs={'class': 'form-control col-md-8'}))
    content = forms.CharField(label="Content of the title", widget=forms.Textarea(attrs={'class': 'form-control col-md-8', 'rows': 8}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "All pages"
    })


def entry(request, entry):
    titleName = util.get_entry(entry)
    if titleName is None:
        return render(request, "encyclopedia/fail.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(titleName),
            "entryTitle": entry
        })


def search(request):
    all_entries = util.list_entries()
    matched_entries = []
    if request.method == "GET":
        query = request.GET.get('query')
        if (util.get_entry(query) is not None):
            return HttpResponseRedirect(reverse("entry", kwargs={'entry': query}))
        else:
            for entry in all_entries:
                if (query in entry.lower()):
                    matched_entries.append(entry)
            return render(request, "encyclopedia/index.html", {
                "entries": matched_entries,
                "title": "Result"
            })


def newPage(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/fail.html")
        else:
            return render(request, "encyclopedia/newPage.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/newPage.html", {
            "form": NewEntryForm()
        })

def edit(request, entry):
    if request.method == "GET":
        entryPage = util.get_entry(entry)
        form = NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/edit.html", {
                "form": form,
                "edit": form.fields["edit"].initial,
                "entryTitle": form.fields["title"].initial
            })
    else:
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))

def randomPage(request):
    entries = util.list_entries()
    random_page = entries[randint(0, len(entries) - 1)]
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': random_page}))