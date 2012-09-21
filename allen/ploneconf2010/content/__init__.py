""" Content
"""
from Products.CMFCore import utils as cmfutils
from Products.Archetypes.atapi import process_types, listTypes

PROJECTNAME = 'allen.ploneconf2010'
ADD_CONTENT_PERMISSION = "Add portal content"

from Products.Archetypes.atapi import registerType
from book import Book

registerType(Book, PROJECTNAME)

def initialize(context):
    """ Zope2 init
    """
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME), PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
