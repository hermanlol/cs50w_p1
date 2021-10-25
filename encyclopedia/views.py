from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2
import pdb;
import random;

class NewTaskForm(forms.Form):
    entry_title = forms.CharField(label="Title")
    entry_content = forms.CharField(widget=forms.Textarea())

class editform(forms.Form):
    edit_content = forms.CharField(widget=forms.Textarea())

def index(request):


    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        #go direct if matching entry
        #find sub list_entries()
        #
    })


def entry(request, entry):
    entries = util.list_entries()
    md = markdown2.Markdown()
    if entry in entries:
        entry_page = util.get_entry(entry)
        return render(request, "encyclopedia/entry.html",{
            "entry":md.convert(entry_page),
            "entry_title":entry
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "entry_title":entry
        })



def search(request):
    #if request.method == "GET":
    search = request.GET.get('q','')
    #print {variable to inspect}
    search_entry = util.get_entry(search)


    if (search_entry is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry' : search}))
    else:
        view_entries = []
        for i in util.list_entries():
            if search.lower() in i.lower():
                view_entries.append(i)
        print(view_entries)
        return render(request, "encyclopedia/index.html",{            
            "search_v": True,
            "entries": view_entries,
            "search_value": search
        })


def create(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            #breakpoint()
            title = form.cleaned_data['entry_title']
            content = form.cleaned_data['entry_content']
            #check = util.get_entry(title)
            #need edit
            #error message if exists
            #
            entries = util.list_entries()
            for i in entries:
                if title.lower() in i.lower():
                        return render(request, "encyclopedia/create.html",{
                            "check": False,
                            "form" : form,
                            "title": title
                        })
            else:
                    util.save_entry(title, content)
                    return HttpResponseRedirect(reverse("entry", kwargs={"entry":title}))

           
    return render(request, "encyclopedia/create.html",{
        "form": NewTaskForm(),
        "check": True
    })

def edit(request, entry):
    #form = NewTaskForm(request.POST)
    
    if request.method == "POST":
        form = editform(request.POST)
        if form.is_valid():
            #breakpoint()
            content = form.cleaned_data['edit_content']
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("entry", kwargs={"entry":entry}))
    
    if request.method == "GET":
        page = util.get_entry(entry)
        #breakpoint()
        if page is not None:
            form = editform(initial={'edit_content': page})
            #breakpoint()
            return render(request, "encyclopedia/edit.html",{
                "entry": entry,
                "form": form,
                "edit": True
            })
        else:
            return render(request, "encyclopedia/error.html")

def random_page(request):
    entries = util.list_entries()
    #breakpoint()
    random_entry = random.choice(entries)
    #breakpoint()
    return HttpResponseRedirect(reverse("entry", kwargs={"entry":random_entry}))