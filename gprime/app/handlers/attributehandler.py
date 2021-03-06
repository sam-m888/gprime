#
# gPrime - a web-based genealogy program
#
# Copyright (c) 2017 gPrime Development Team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import tornado.web

from .handlers import BaseHandler
from ..forms import AttributeForm

class AttributeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, prefix="", suffix=""):
        """
        prefix = 'person/b2cfa6ca14d1f274465'
        suffix = '1', or '1/delete' add, or edit
        """
        _ = self.app.get_translate_func(self.current_user)
        if "/" in suffix:
            row, action = suffix.split("/")
        else:
            row, action = suffix, "view"
        # prefix: 'person/d7f407bcd41d568c68ae798b71/media_list/0'
        # suffix: '1'
        instance = self.app.get_object_from_url(prefix)
        path = "attribute_list.%s" % (int(row) - 1)
        if prefix.count("/") > 2:
            parts = prefix.split("/") # "/person/handle/somethings/", ["", "person", "handle", "sometings"]
            path = ".".join(parts[2:]) + "." + path
        url = "/" + prefix + "/attribute_list/" + row
        subitem = instance.get_field(path)
        form = AttributeForm(self, instance, subitem, path, url)
        ## FIXME: Handle add and delete
        self.render("attribute.html",
                    **self.get_template_dict(tview=_("attribute"),
                                             action=action,
                                             search="",
                                             page="",
                                             form=form))
        return

    @tornado.web.authenticated
    def post(self, prefix="", suffix=""):
        """
        prefix = 'person/b2cfa6ca14d1f274465'
        suffix = '1'
        """
        _ = self.app.get_translate_func(self.current_user)
        if "/" in suffix:
            row, action = suffix.split("/")
        else:
            row, action = suffix, "view"
        # prefix: 'person/d7f407bcd41d568c68ae798b71/media_list/0'
        # suffix: '1'
        instance = self.app.get_object_from_url(prefix)
        path = "attribute_list.%s" % (int(row) - 1)
        if prefix.count("/") > 2:
            parts = prefix.split("/") # "/person/handle/somethings/", ["", "person", "handle", "sometings"]
            path = ".".join(parts[2:]) + "." + path
        url = "/" + prefix + "/attribute_list/" + row
        subitem = instance.get_field(path)
        form = AttributeForm(self, instance, subitem, path, url)
        form.save()
        self.redirect(self.app.make_url(url))
