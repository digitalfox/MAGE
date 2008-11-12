# coding: utf-8

# Python imports
import os
import unicodedata

# Django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.core.urlresolvers import reverse

# MAGE imports
from graphs import getGraph, DrawingContext
from MAGE.ref.models import Environment, MageModelType, Component

def full_pic(request):
    """Carte de l'ensemble des composants référencés"""
    # Create png with GraphWiz  
    png = getGraph()
    
    # Return the picture
    return HttpResponse(png, mimetype="image/png")

def filter_pic(request, nbParents, nbPartners, collapseThr): 
    dico = request.GET
    filter = {}

    for fi in dico.keys():
        filter[unicodedata.normalize('NFKD', fi).encode('ascii','ignore')] = [int(i) for i in dico[fi].split(',')]
    
    # Create png with GraphWiz  
    dc = DrawingContext()
    dc.parentRecursionLevel = int(nbParents)
    dc.patnersRecursionLevel = int(nbPartners)
    dc.components = Component.objects.filter(**filter)
    dc.collapse_threshold = int(collapseThr)
    png = dc.render()
    
    # Return the picture
    return HttpResponse(png, mimetype="image/png")


def envt_pic(request, envt_id):
    # Create png with GraphWiz  
    dc = DrawingContext()
    dc.parentRecursionLevel = 0
    dc.patnersRecursionLevel = 5
    dc.components = Component.objects.filter(environments__pk=envt_id)
    dc.collapse_threshold = 5
    png = dc.render()
    
    # Return the picture
    return HttpResponse(png, mimetype="image/png")

class CartoForm(forms.Form):
    envts = forms.MultipleChoiceField(
                    choices = [(e.pk, e.name) for e in Environment.objects.all()], 
                    widget = forms.widgets.CheckboxSelectMultiple,
                    initial = [e.pk for e in Environment.objects.all()],
                    label = u'Environnements à afficher')
    
    models = forms.MultipleChoiceField(
                    choices = [(m.pk, m.name) for m in MageModelType.objects.all()], 
                    widget = forms.widgets.CheckboxSelectMultiple,
                    initial = [m.pk for m in MageModelType.objects.all()],
                    label = u'Composants à afficher')
    
    parentRecursion = forms.IntegerField(
                    label = u'Générations de parents à afficher ',
                    max_value=3,
                    min_value=0,
                    initial=0)
    
    partnerRecursion = forms.IntegerField(
                    label = u'Récursion sur les partenaires ',
                    max_value=20,
                    min_value=0,
                    initial=0)
    
    collapseThr = forms.IntegerField(
                    label = u'Réunir éléments similaires à partir de ',
                    max_value=20,
                    min_value=0,
                    initial=2)
    
    

def view_carto(request):
    """Marsupilamographe"""
    if request.method == 'POST':            # If the form has been submitted...
        form = CartoForm(request.POST)      # A form bound to the POST data
        if form.is_valid():                 # All validation rules pass
            # Process the data in form.cleaned_data
            filter={}
            filter['environments__pk__in'] = form.cleaned_data['envts']
            ad = reverse('MAGE.gph.views.filter_pic', 
                         args=(str(form.cleaned_data['parentRecursion']),
                               str(form.cleaned_data['partnerRecursion']),
                               str(form.cleaned_data['collapseThr']))) + '?environments__pk__in=' 
            for env in form.cleaned_data['envts']: ad += env + ','
            ad = ad[:-1] + ';model__pk__in='
            for pk in form.cleaned_data['models']: ad += pk + ","
            ad = ad[:-1]
            
            return render_to_response('view_carto.html',  {'resultlink': ad, 'machin':'truc', 'form': form,})
    else:
        form = CartoForm() # An unbound form

    return render_to_response('view_carto.html',  {'form': form,})
