# Nemo Nautilus Admin - Extension for Nautilus to do administrative operations
# Copyright (C) 2024 Kevin Kim <chaeya@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, subprocess
import mimetypes

from gi import require_version
require_version('Nemo', '3.0')  

from gi.repository import Nemo, GObject  
from gettext import gettext as _, bindtextdomain, textdomain
try:
    # python 8
    from gettext import locale
except ImportError:
    # python 9
    import locale

import gettext
import locale

ROOT_UID = 0
NEMO_PATH = "@NEMO_PATH@"  
XED_PATH = "@XED_PATH@"  

class NemoAdmin(Nemo.MenuProvider, GObject.GObject):  # 변경: Nautilus -> Nemo
    """Simple Nemo extension that adds some administrative (root) actions to
    the right-click menu, using GNOME's new admin backend."""
    def __init__(self):
        self._setup_gettext()

    def _setup_gettext(self):
        """Setup gettext to use the nemo-admin domain."""
        locale.setlocale(locale.LC_ALL, '')
        bindtextdomain('nemo-admin', '/usr/share/locale')
        textdomain('nemo-admin')
        _ = gettext.gettext

    def get_file_items(self, *args):
        """Returns the menu items to display when one or more files/folders are
        selected."""
        files = args[-1]
        self._setup_gettext()
        # Don't show when already running as root, or when more than 1 file is selected
        if os.geteuid() == ROOT_UID or len(files) != 1:
            return
        file = files[0]

        # Add the menu items
        items = []
        if file.get_uri_scheme() == "file": # must be a local file/directory
            if file.is_directory():
                if os.path.exists(NEMO_PATH):
                    # items += [self._create_nemo_item(file)]  
                    pass                
            else:
                mime_type = file.get_mime_type()
                if os.path.exists(XED_PATH) and (mime_type.startswith("text/") or mime_type in ["application/xml", "application/json", "application/x-shellscript", "application/xhtml+xml"]):
                    items += [self._create_xed_item(file)]  # Add xed item if mime type is editable by xed
                if os.access(file.get_location().get_path(), os.X_OK):
                    items += [self._create_exec_item(file)]  # Add exec item if file is executable

        return items

    def get_background_items(self, *args):
        """Returns the menu items to display when no file/folder is selected
        (i.e. when right-clicking the background)."""
        file = args[-1]
        # Don't show when already running as root
        if os.geteuid() == ROOT_UID:
            return

        # Add the menu items
        items = []
        if file.is_directory() and file.get_uri_scheme() == "file":
            if os.path.exists(NEMO_PATH):
                # hide this item
                # items += [self._create_nemo_item(file)]  
                pass

        return items

    def _create_nemo_item(self, file):  
        """Creates the 'Open as Administrator' menu item."""
        item = Nemo.MenuItem(name="NemoAdmin::Nemo",  
                             label=_("Open as A_dministrator"),
                             tip=_("Open this folder with root privileges"),
                             icon="folder")
        item.connect("activate", self._nemo_run, file)  
        return item

    def _nemo_run(self, menu, file):  
        """'Open as Administrator' menu item callback."""
        uri = file.get_uri()
        admin_uri = uri.replace("file://", "admin://")
        subprocess.Popen([NEMO_PATH, admin_uri])

    def _create_xed_item(self, file):  
        """Creates the 'Edit as Administrator' menu item."""
        item = Nemo.MenuItem(name="NemoAdmin::Xed",  
                             label=_("Edit as A_dministrator"),
                             tip=_("Open this file in the text editor with root privileges"),
                             icon="text-editor")
        item.connect("activate", self._xed_run, file)  
        return item

    def _xed_run(self, menu, file):  
        """'Edit as Administrator' menu item callback."""
        uri = file.get_uri()
        admin_uri = uri.replace("file://", "admin://")
        subprocess.Popen([XED_PATH, admin_uri])

    def _create_exec_item(self, file):
        """Creates the 'Run as Administrator' menu item."""
        item = Nemo.MenuItem(name="NemoAdmin::Exec",
                             label=_("Run as A_dministrator"),
                             tip=_("Run this file with root privileges"),
                             icon="application-x-executable")
        item.connect("activate", self._exec_run, file)
        return item

    def _exec_run(self, menu, file):
        """'Run as Administrator' menu item callback."""
        path = file.get_location().get_path()
        subprocess.Popen(['gnome-terminal', '-v', '--window', '--', '/bin/zsh', '-c', f"pkexec {path} ; exec /bin/zsh", '--working-directory', os.path.dirname(path)])

    def get_name_and_desc(self):
        description = _("Open as A_dministrator")
        return [(f"nemo-admin:::{description}")]