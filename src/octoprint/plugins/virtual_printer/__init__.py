# coding=utf-8
from __future__ import absolute_import

__author__ = "Gina Häußge <osd@foosel.net>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2015 The OctoPrint Project - Released under terms of the AGPLv3 License"

import octoprint.plugin

class VirtualPrinterPlugin(octoprint.plugin.SettingsPlugin):

    def virtual_printer_factory(self, comm_instance, port, baudrate, read_timeout):
        if not port == "VIRTUAL":
            return None

        if not self._settings.global_get_boolean(["devel", "virtualPrinter", "enabled"]):
            return None

        import logging
        import logging.handlers

        seriallog_handler = logging.handlers.RotatingFileHandler(self._settings.get_plugin_logfile_path(postfix="serial"), maxBytes=2*1024*1024)
        seriallog_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        seriallog_handler.setLevel(logging.DEBUG)

        from . import virtual
        serial_obj = virtual.VirtualPrinter(seriallog_handler=seriallog_handler, read_timeout=float(read_timeout))
        return serial_obj

__plugin_name__ = "Virtual Printer"
__plugin_author__ = "Gina Häußge, based on work by Daid Braam"
__plugin_homepage__ = "https://github.com/foosel/OctoPrint/wiki/Plugin:-Virtual-Printer"
__plugin_license__ = "AGPLv3"
__plugin_description__ = "Provides a virtual printer via a virtual serial port for development and testing purposes"

def __plugin_load__():
    plugin = VirtualPrinterPlugin()

    global __plugin_implementation__
    __plugin_implementation__ = plugin

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.comm.transport.serial.factory": plugin.virtual_printer_factory
    }
