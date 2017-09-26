## Fonty Python Copyright (C) 2017 Donn.C.Ingle
## Contact: donn.ingle@gmail.com - I hope this email lasts.
##
## This file is part of Fonty Python.
## Fonty Python is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Fonty Python is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Fonty Python.  If not, see <http://www.gnu.org/licenses/>.
import locale
import strings
import linux_safe_path_library
LSP = linux_safe_path_library.linuxSafePath()

"""
testing i18n with fontybugs
try:
    raise fontybugs.BadVoodoo("bad voodoo")
except fontybugs.BadVoodoo, e:
    print "error:", unicode(e)
try:
    raise fontybugs.PogWriteError("/some/path/po.pog")
except fontybugs.PogWriteError, e:
        print unicode(e)
"""

## The %s must be OUTSIDE the _() construct.
class Errors ( Exception ):
    checkperms = _("\n(Also check your file permissions.)")
    messages = {
    001 : _("Bad voodoo error. I give up."),
    100 : _("There is no such item."),
    200 : _("Pog is empty."),
    300 : _("Pog is already installed."),
    500 : _("Pog cannot be written to.\nCheck your filesystem.%s") % checkperms,
    600 : _("Pog is invalid, please hand-edit it."),
    700 : _("Some fonts did not install.\nPerhaps the original fonts folder has moved or been renamed.\nYou should purge or hand-edit."),
    800 : _("Pog is not installed."),
    900 : _("Some fonts could not be uninstalled.\nPlease check your home .fonts (with a dot in front) folder for broken links.%s") % checkperms,
    1000 : _("Cannot delete the Pog.%s") % checkperms,
    1010 : _("Not a single font in this pog could be installed.\nThe original font folder has probably moved or been renamed."),
    1020 : _("Not a single font in this pog could be uninstalled.\nNone of the fonts were in your fonts folder, please check your home .fonts (with a dot in front) folder for broken links.\nThe pog has been marked as \"not installed\"."),
    1030 : _("This folder has no fonts in it."),
    }

    def __unicode__( self ):
        return u"%s : %s" % ( self.__class__.messages[self._id], self._item )

    def _format_error(self):
        ## As of Python 2.6 e.message has been deprecated.
        ## Turn 'self' into a 'string like object' by calling __unicode__ above.
        msg = unicode(self)
        msg = fpsys.LSP.to_bytes( msg )
        return msg

    def unicode_of_error(self):
        """For use in wx gui when I am going to print the error in a messagebox."""
        return self._format_error()

    def print_error(self):
        print self._format_error()

    def print_error_and_quit(self):
        print self._format_error()
        raise SystemExit


class BadVoodoo ( Errors ):
    def __init__ ( self, item = None):
        self._item = item
        self._id = 001

class ErrNoSuchItem ( Errors ):
    def __init__ ( self, item = None):
        self._item = item
        self._id = 100

class PogEmpty ( Errors ):
    def __init__ ( self, item = None):
        self._item = item
        self._id = 200

class PogInstalled ( Errors ):
    def __init__ ( self, item = None):
        self._item = item
        self._id = 300

class PogWriteError ( Errors ):
    def __init__ ( self, item = None):
        self._item = item
        self._id = 500

class PogInvalid ( Errors ):
    def __init__ ( self, item = None):
        self._item = item
        self._id = 600

class PogSomeFontsDidNotInstall ( Errors ): #Some fonts did get installed, but not all
    def __init__ ( self, item = None):
        self._item = item
        self._id = 700

class PogNotInstalled ( Errors ):
    def __init__ ( self, item = None):
        self._item = item
        self._id = 800

class PogLinksRemain ( Errors ):
    def __init__ ( self, item = None):
        self._item = item
        self._id = 900

class PogCannotDelete ( Errors ):
    def __init__ ( self, item = None):
        self._item = item
        self._id = 1000

class PogAllFontsFailedToInstall ( Errors ):
    def __init__ ( self, item = None):
        self._item = item
        self._id = 1010

class PogAllFontsFailedToUninstall ( Errors ):
    def __init__ ( self, item = None):
        self._item = item
        self._id = 1020

class FolderHasNoFonts ( Errors ):
    def __init__ ( self, item = None):
        self._item = item
        self._id = 1030

## Sept 2017
## Some new errors.
## These errors take a path argument so their unicode
## can display that path in the error message.
## They also take an "associated_err" which is an error object
## (Probably an OSError of some kind.)
class NoFontypythonDir(Errors):
    def __init__(self,path, associated_err):
        self.path = path #LSP.ensure_unicode(path)
        self.associated_err = associated_err #LSP.ensure_unicode(associated_err)
    def __unicode__(self):
        return _(u"The \"fontypython\" directory within %(path)s cannot be \
                created or found.\nFonty cannot run until it exists. \
                Please create it, and start me again.\
                \n\nExample:\n\tcd %(path)s\n\tmkdir fontypython\
                \n\n[Extra: %(assocerr)s]") % {"path":self.path, "assocerr":associated_err}

class NoFontsDir(Errors):
    def __init__(self,path, associated_err):
        self.path = path # LSP.ensure_unicode(path)
    def __unicode__(self):
        return _(u"The main \"fonts\" directory within \
                %(path)s is missing.\nFonts cannot be installed until it exists.\
                Please create it, and start me again.\
                \n\nExample:\n\tcd %(path)s\n\tmkdir fonts\
                \n\n[Extra: %(assocerr)s]") % {"path":self.path, "assocerr":associated_err}

class UpgradeFail(Errors):
    """
    Any and all UpgradeFail errors should end the app after being caught.
    """
    def __init__(self, msg, associated_err):
        self.msg = msg #LSP.ensure_unicode(msg)
        self.associated_err = associated_err # LSP.ensure_unicode(associated_err)
    def __unicode__(self):
        return _(u"Upgrade Error.\n{}\n\n[Extra:{}]").format(self.msg, associated_err)



