from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from ..enums.deprel_enum import Deprel
from treeflow.corpus.models import (
    BibEntry,
   
)  # Adjust to your model's import path
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
import requests
import json

# import django generic views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# import django forms
from django import forms

# import generic form view
from django.views.generic.edit import FormView

# create a generic view function for BibEntry
class BibEntryListView(ListView):
    model = BibEntry
    paginate_by = 10
    template_name = 'bibentry_list.html'

    def get_queryset(self):
        return BibEntry.objects.order_by('key')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Bibliography'
        # context['zotero_data'] = self.get_zotero_data()
        return context

    # create a function to use the requests library to get the data from the zotero api with the object keys
    def get_zotero_data(self, **kwargs):
        # get the object keys from the queryset
        object_keys = self.get_queryset().values_list('key', flat=True)
        # create a list to store the data
        data = []
        # loop through the object keys and get the data from the zotero api
        url = 'https://api.zotero.org/groups/2116388/collections/SGLY6KYR/items/'
        r = requests.get(url)
        r = r.json()
        
        data.append(r)
        data = data[0]
        # return the data
        return data

# create a generic create view for BibEntry

class BibEntryCreateView(CreateView):
    model = BibEntry
    fields = '__all__'  # Or specify the fields you want to include in the form
    template_name = 'bibentry_create.html'  # Specify the template for the create view
    success_url = '/corpus/bibliography'  # Specify the URL to redirect to after successful creation
