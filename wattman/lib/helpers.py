"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""

from routes import url_for
from webhelpers.html import literal
from webhelpers.html.secure_form import secure_form
from webhelpers.html.tags import *
from webhelpers.html.tools import auto_link, mail_to
from webhelpers.text import truncate, chop_at, plural

from webhelpers.html.tags import stylesheet_link
from webhelpers.html.tags import javascript_link

from authkit.authorize.pylons_adaptors import authorized
from authkit.permissions import RemoteUser, ValidAuthKitUser, UserIn
