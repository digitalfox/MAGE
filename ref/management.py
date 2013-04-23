# coding: utf-8
'''
Created on 10 mars 2013

@author: Marc-Antoine
'''

## Python imports

## Django imports
from django.db.models.signals import post_syncdb
from django.contrib.auth.models import Group, User, Permission

## MAGE imports
import models
from prm.models import setParam, getMyParams

def post_syncdb_handler(sender, **kwargs):
    # Create parameters
    if getMyParams().count() == 0:
        setParam(key = u'LINK_WHO', value = u'Qui est l\'équipe technique ? <br/>(Confluence)', 
                 default_value = u'Qui est l\'équipe technique ? <br/>(Confluence)', 
                 description = u'Texte bouton de la page d\'accueil',
                 axis1 = u'Technical team links')
        setParam(key = u'LINK_WHO_URL', value = u'http://www.google.com/ncr', 
                 default_value = u'http://www.google.com/ncr', 
                 description = u'URL du lien WHO',
                 axis1 = u'Technical team links url')
        setParam(key = u'LINK_WHAT', value = u'Que fait l\'équipe technique pour les utilisateurs ?<br/>(Confluence)', 
                 default_value = u'Que fait l\'équipe technique pour les utilisateurs ?<br/>(Confluence)', 
                 description = u'Texte bouton de la page d\'accueil',
                 axis1 = u'Technical team links')
        setParam(key = u'LINK_WHAT_URL', value = u'http://www.google.com/ncr', 
                 default_value = u'http://www.google.com/ncr', 
                 description = u'URL du lien WHAT',
                 axis1 = u'Technical team links url')
        setParam(key = u'LINK_BUGTRACKER', value = u'Faire une demande à l\'équipe technique<br/>(JIRA)', 
                 default_value = u'Faire une demande à l\'équipe technique<br/>(JIRA)', 
                 description = u'Texte bouton de la page d\'accueil',
                 axis1 = u'Technical team links')
        setParam(key = u'LINK_BUGTRACKER_URL', value = u'http://www.google.com/ncr', 
                 default_value = u'http://www.google.com/ncr', 
                 description = u'URL du lien BUG',
                 axis1 = u'Technical team links url')
        
        setParam(key = u'LINK_COLORS', value = u'#004D60,#1B58B8,#DE4AAD', 
                 default_value = u'#004D60,#1B58B8,#DE4AAD', 
                 description = u'Couleurs des cases de la page d\'accueil')
        
        setParam(key = u'MODERN_COLORS', value = u'#004A00,#61292B,#180052,#AD103C,#004D60,#1B58B8,#DE4AAD', 
                 default_value = u'#004A00,#61292B,#180052,#AD103C,#004D60,#1B58B8,#DE4AAD', 
                 description = u'Couleurs des cases de la page d\'accueil')

    
    
## Listen to the syncdb signal
post_syncdb.connect(post_syncdb_handler, sender=models)