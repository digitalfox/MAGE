# coding: utf-8
'''
    @license: Apache License, Version 2.0
    @copyright: 2007-2013 Marc-Antoine Gouillart
    @author: Marc-Antoine Gouillart
'''

## Python imports
import re

## Django imports
from django import forms
from django.forms import ModelForm

## MAGE imports
from scm.models import Delivery, LogicalComponentVersion, InstallableItem, ItemDependency, InstallationMethod
from ref.models import LogicalComponent
from ref.widgets import ClearableFileInputPretty
from django.forms.models import ModelChoiceField


class DeliveryForm(ModelForm):
    def clean_ticket_list(self):
        data = self.cleaned_data['ticket_list']
        if len(data) == 0:
            return data
        p = re.compile('([\da-zA-Z_-]+,?)+$')
        if p.match(data) is None:
            raise forms.ValidationError("This field must be a comma-separated list of ticket ID (letters and integers)")
        return data

    class Meta:
        model = Delivery
        exclude = ['removed', 'status', ]
        widgets = { 'datafile': ClearableFileInputPretty}

class LcChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.application.name, obj.name)

class IIForm(ModelForm):
    #target = LcChoiceField(queryset=LogicalComponent.objects.filter(implemented_by__installation_methods__restoration_only = False, implemented_by__installation_methods__available = True).annotate(num_methods=Count('implemented_by__installation_methods')).filter(scm_trackable=True).filter(num_methods__gt = 0).order_by('application__name', 'name'), label='Composant livré')
    target = LcChoiceField(queryset=LogicalComponent.objects.all())
    # TODO: make query right
    version = forms.CharField(label='Version livrée')

    def save(self, commit=True):
        logicalcompo = self.cleaned_data['target']
        version = self.cleaned_data['version']
        v = LogicalComponentVersion.objects.get_or_create(logical_component=logicalcompo, version=version)[0]
        v.save()
        self.instance.what_is_installed = v
        o = super(IIForm, self).save(commit)
        return o

    def clean_how_to_install(self):
        data = self.cleaned_data['how_to_install']
        deleted = self.cleaned_data.has_key('DELETE') if self.cleaned_data.has_key('DELETE') else False
        if len(data) == 0 and not deleted:
            raise forms.ValidationError("At least one technical target is required")
        return data

    def clean_datafile(self):
        dfile = self.cleaned_data['datafile']
        try:
            target = self.cleaned_data['target']
        except KeyError:
            return dfile
        methods = self.cleaned_data['how_to_install']

        if len(methods) == 0:
            return dfile
        for method in methods:
            if method.checkers.count() > 0 and (dfile is None or dfile == False):
                raise forms.ValidationError('A datafile is required')
        if dfile == False: ## Cleared file
            return dfile

        for method in methods:
            method.check_package(dfile, target)
        return dfile

    def clean(self):
        cleaned_data = super(IIForm, self).clean()

        ## Check how_to_install consistency
        if self.cleaned_data.has_key('target') and self.cleaned_data.has_key('how_to_install'):
            logicalcompo = self.cleaned_data['target']
            htis = self.cleaned_data['how_to_install']
            for hti in htis:
                if not logicalcompo in [i.implements for i in hti.method_compatible_with.all()]:
                    raise forms.ValidationError("Inconsistent choice - that method is not compatible with this target")

        ## Check datafile according to hpow_to_install
        ##self.clean_datafile2()

        ## Done
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(IIForm, self).__init__(*args, **kwargs)
        self.fields['how_to_install'].queryset = InstallationMethod.objects.filter(restoration_only=False)

        if kwargs.has_key('application'):
            self.field['target'].queryset = self.field['target'].queryset.filter(application=kwargs['application'])
            kwargs.remove('application')

        if self.instance != None and self.instance.pk is not None:
            self.initial['target'] = self.instance.what_is_installed.logical_component.pk
            self.initial['version'] = self.instance.what_is_installed.version

    class Meta:
        model = InstallableItem
        # exclude = ['what_is_installed',]
        fields = ('target', 'version', 'how_to_install', 'is_full', 'data_loss', 'datafile')  # 'what_is_installed')
        widgets = { 'datafile': ClearableFileInputPretty}


class IDForm(ModelForm):
    #target = LcChoiceField(queryset=LogicalComponent.objects.filter(scm_trackable=True, implemented_by__installation_methods__isnull=False).distinct().order_by('application__name', 'name'), label='dépend de ', required=False)
    target = LcChoiceField(queryset=LogicalComponent.objects.all())
    # TODO: make query right

    class Meta:
        model = ItemDependency
        fields = ('target', 'depends_on_version', 'operator',)


