from audioop import reverse
from multiprocessing.sharedctypes import Value
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from markdown import Markdown
from django.urls import reverse
from django import forms
import secrets    
from django.contrib.auth.decorators import login_required

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    markdowner = Markdown()
    EntryPage = util.get_entry(entry)
    if EntryPage is None:
        return render (request, "encyclopedia/notexisting.html", {
            "EntryTitle": entry
        })
    else:
        return render (request, "encyclopedia/entry.html", {
            "entry":markdowner.convert(EntryPage),
            "EntryTitle": entry
        })


def search(request):
    value = request.GET.get('q', '')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs ={'entry': value }))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)

        return render(request, "encyclopedia/index.html", {
        "search": True,
        "entries": subStringEntries,
        "value": value
        })

def edit(request, entry):
    EntryPage = util.get_entry(entry)
    if EntryPage is None:
        return render(request, "encyclopedia/notexisting.html", {
            "EntryTitle": entry
        })
    else:
        form = NewEntry()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = EntryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newEntry.html", {
            "form": form,
            "edit": True,
            "EntryTitle": form.fields["title"].initial
        })

class NewEntry(forms.Form):
    title = forms.CharField(label="Entry Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows':15}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def newEntry(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            if(util.get_entry(title)is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry':title}))
            else:
                return render(request, "encyclopedia/newEntry.html",{
                    "form":form,
                    "existing":True,
                    "entry":title 
                })

        else:
            return render(request, "encyclopedia/newEntry.html",{
                    "form":form,
                    "existing":False
                })
    else:
        return render(request, "encyclopedia/newEntry.html",{
                    "form":NewEntry(),
                    "existing":False
        })

def random(request):
    entries=util.list_entries()
    RandomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry':RandomEntry}))