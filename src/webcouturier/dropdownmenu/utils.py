import logging

from zope.component import getUtility
from Products.CMFCore.interfaces import IPropertiesTool

logger = logging.getLogger("webcouturier.dropdownmenu")

def getDropdownDepth():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('dropdown_depth')


def cachingEnabled():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('enable_caching', False)


def parentClickable():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('enable_parent_clickable', True)

try:
    # BBB with old Plones
    from .menusettings import getMenuSettings

    def getMenuItemIds(context):
        """
        Get visible menu items and their order on the content item.

        1) Return all content item ids if there are no menu settings (IMenuSettings)

        2) Otherwise return content item ids defined to be visible

        :return: None if to show all ids, otherwise the filtered in id list
        """
        storage = getMenuSettings(context)
        if storage.menuItems:
            return storage.menuItems
        return None

except ImportError as e:

    logger.warn("Dropdownmenu settings disabled")

    def getMenuItemIds(context):
        # Fallback to return all items always on old systems
        return None
