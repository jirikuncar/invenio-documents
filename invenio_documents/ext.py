# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Invenio module for document management."""

from __future__ import absolute_import, print_function

from flask import current_app
from werkzeug.utils import import_string

from .api import Document
from .cli import documents as cmd


class InvenioDocuments(object):
    """Invenio-Documents extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        app.extensions['invenio-documents'] = self
        app.cli.add_command(cmd)

    def init_config(self, app):
        """Initialize configuration."""
        # Getter method has to be provided.
        app.config.setdefault('DOCUMENTS_GETTER', None)

    def get_document(self, record, filename):
        """Return an instance of Document guessed by ``DOCUMENTS_GETTER``."""
        getter = current_app.config['DOCUMENT_GETTER']
        if getter is not None and not callable(getter):
            getter = import_string(getter)
        res = getter(record, filename)
        if res is not None:
            pointer, _ = res
            return Document(record, pointer)
