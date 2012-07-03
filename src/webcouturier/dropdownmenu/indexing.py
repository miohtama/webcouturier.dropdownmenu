"""

    Define custom portal_catalog indexes and metadata columns.

"""

from Products.CMFCore.interfaces import IFolderish
from plone.indexer.decorator import indexer

from webcouturier.dropdownmenu.utils import getMenuItemIds


@indexer(IFolderish)
def menu_items(object, **kw):
    """ Populate menu_items metadata in portal_catalog

    """
    items = getMenuItemIds(object)
    return items
