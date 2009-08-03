# coding: utf-8

"""
    MAGE Unix server sample module models file.
    
    @author: Marc-Antoine Gouillart
    @contact: marsu_pilami@msn.com
    @license: GNU GVL v3
"""

###########################################################
## Server
###########################################################

from django.db import models
from MAGE.ref.models import Component
from MAGE.ref.admin import ComponentAdmin
from django.contrib import admin

class Server(Component):
    OS_CHOICES = (
                  ('Windows 2003', 'Windows 2003'),
                  ('Windows 2008', 'Windows 2008'),
                  ('Windows Vista', 'Windows Vista'),
                  ('Windows 7', 'Windows 7'),
                  ('AIX 5.3', 'AIX 5.3'),
                  ('AIX 5.4', 'AIX 5.4'),
                  ('AIX 6.1', 'AIX 6.1'),
                  ('Linux', 'Linux'),
                  ('HPUX vn', 'HPUX vn'),
                  )
    os          = models.CharField(max_length=30, choices=OS_CHOICES, verbose_name='OS ')
    comment     = models.CharField(max_length=200, blank=True, null=True, verbose_name='Commentaire')
    ip1         = models.IPAddressField(verbose_name='IP1 ')
    ip2         = models.IPAddressField(blank=True, null=True, verbose_name='IP2 ')
    ip3         = models.IPAddressField(blank=True, null=True, verbose_name='IP3 ')
    ip4         = models.IPAddressField(blank=True, null=True, verbose_name='IP4 ')
    parents = {'papa':'Server',}
    
    def __unicode__(self):
        return "Serveur (%s) %s " %(self.os, self.instance_name)
    
    class Meta:
        verbose_name = u'Serveur'
        verbose_name_plural = u'Serveurs'
        
    def _isVM(self):
        try:
            self.papa
        except:
            return False
        return True
    isvm = property(_isVM)
    _isVM.boolean = True


class ServerAdmin(ComponentAdmin):
    ordering = ('instance_name',)
    list_display = ('instance_name', 'comment','_isVM')
    fieldsets = [
        ('Informations génériques',  {'fields': ['connectedTo', 'dependsOn']}),
        ('Spécifique Serveur',       {'fields': ['instance_name', 'comment', 'ip1', 'ip2', 'ip3', 'ip4', 'os']}),
    ]
admin.site.register(Server, ServerAdmin)
