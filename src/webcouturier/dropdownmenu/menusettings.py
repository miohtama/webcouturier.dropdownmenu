"""

    Configure folder visible menu items.

"""

# Zope imports
from Products.CMFCore.interfaces import IFolderish
from five import grok
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder

# Plone imports
from plone.directives import form
from plone.behavior.annotation import AnnotationsFactoryImpl

# Local imports
from webcouturier.dropdownmenu import _


def make_terms(items):
    """ Create zope.schema terms for vocab from tuples """
    terms = [SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items]
    return terms


@grok.provider(IContextSourceBinder)
def folder_items(context):
    """
    Populate vocabulary with folder content items.

    @param context: AnnotationsFactoryImpl

    @return: SimpleVocabulary containg all areas as terms.
    """

    # We must peek through storage layer to get the
    # underlying content context item

    folder = context.annotations.obj

    items = folder.listFolderContents()

    def show(item):
        """
        """
        # Note: getExcludeFromNav not necessarily exist on all content types
        if hasattr(item, "getExcludeFromNav"):
            if item.getExcludeFromNav():
                return False
        return True

    terms = [(item.getId(), item.Title()) for item in items if show(item) == True]
    # Convert tuples to SimpleTerm objects
    terms = make_terms(terms)

    return SimpleVocabulary(terms)


class IMenuSettings(form.Schema):
    """
    Store per-folder menu settings in annotations.
    """

    #: Stores list of visibl menu items and their order for this folderish content item.
    menuItems = schema.List(value_type=schema.Choice(source=folder_items),
        title=_(u"Available menu items"),
        description=_(u"Dropdown menu items shown for this folder. Leave empty to display the full folder contents always.")
        )


def getMenuSettings(context):
    """
    Return the object used to store menu setting on a content item.

    AnnotationsFactoryImpl makes sure that we don't store IMenuSettings
    class reference on persistent objects, meaning that we don't break things
    even though webcouturier.dropdownmenu .py code disappears from the site.
    """

    # We need to have acquisition chain intact because of edit vocab
    return AnnotationsFactoryImpl(context.aq_inner, IMenuSettings)


class MenuSettingsForm(form.SchemaEditForm):
    """
    Form to edit per-folder menu settings.
    """
    grok.context(IFolderish)
    grok.require('cmf.ModifyPortalContent')
    grok.name("menu-settings")

    schema = IMenuSettings

    def getContent(self):
        """
        AnnotationsFactoryImpl makes sure that we don't store IMenuSettings
        class reference on persistent objects, meaning that we don't break things
        even though webcouturier.dropdownmenu .py code disappears from the site.
        """
        return getMenuSettings(self.context)

    def applyChanges(self, data):
        form.SchemaEditForm.applyChanges(self, data)

        # Reflect new data in portal_catalog
        self.context.reindexObject(idxs=["menu_items"])
