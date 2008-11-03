# coding: utf-8

from django.db import models
from MAGE.gcl.models import InstallableSet
from MAGE.ref.models import Component
from django.contrib import admin


###########################################################
## Livraisons
###########################################################

class Delivery(InstallableSet):
    release_notes = models.CharField(max_length=400)
    validation = models.DateField(verbose_name='Date de validation', blank=True, null=True)
    
    def __unicode__(self):
        return u'Livraison %s' %(self.name)


class DeliveryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Identification',  {'fields': ['name', 'ticket']}),
        ('Concerne',        {'fields': ['acts_on']}),
        ('Dépendances',     {'fields': ['is_full']}),
        ('Divers',          {'fields': ['release_notes']}),
    ]
admin.site.register(Delivery, DeliveryAdmin)