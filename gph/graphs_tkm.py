# coding: utf-8

## MAGE imports
from helpers import MageDC
from MAGE.tkm.models import Workflow, State, Transition, Condition

## PYDOT imports
from pydot import Node, Edge

def drawWorkflow(wkf):
    ## Args resolution (raises exceptions)
    if not isinstance(wkf, Workflow):
        raise TypeError('%s n\'est pas un workflow' %wkf)

    ## Create a drawing context
    dc = MageDC()
    
    ## Build nodes
    for state in wkf.choices.all():
        ## Node itself
        n = Node(state.pk)
        n.set_label(dc.encode(state.elt))
        
        ## Add the node to the graph
        dc.add_node(n)
    
        ## Links
        for tr in state.state.transitions_out.all():
            e = Edge(n, Node(tr.target_state.pk))
            dc.add_edge(e)
        
    ## Return the graph
    return dc.render()