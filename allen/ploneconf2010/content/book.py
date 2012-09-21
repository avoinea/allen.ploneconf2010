""" Book """

from Products.Archetypes import atapi
from Products.ATContentTypes.content.document import ATDocument

SCHEMA = ATDocument.schema.copy() + atapi.Schema((
    atapi.StringField('isbn',
        schemata='book',
        widget=atapi.StringWidget(
            label=u'ISBN',
            description=u'ISBN'
        )),
    atapi.StringField('link',
        schemata='book',
        widget=atapi.StringWidget(
            label=u'Link',
            description=u'Book details'
        )),
    atapi.StringField('publisher',
        schemata='book',
        widget=atapi.StringWidget(
            label=u'Publisher',
            description=u'Book publisher'
        )),
    atapi.IntegerField('rating',
        schemata='book',
        widget=atapi.IntegerWidget(
            label=u'Rating',
            description=u'Book rating'
        )),
))

class Book(ATDocument):
    """ Demo Book
    """
    archetypes_name = meta_type = portal_type = 'Book'
    _at_rename_after_creation = True
    schema = SCHEMA
