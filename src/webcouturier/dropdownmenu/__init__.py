from AccessControl import allow_module

allow_module('webcouturier.dropdownmenu.utils')

from zope.i18nmessageid import MessageFactory

_ = MessageFactory("plone")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
