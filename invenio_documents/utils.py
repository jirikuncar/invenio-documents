# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
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

"""Utility functions for serving documents."""

from flask import send_file
from six import StringIO


def send_document(document, mode='rb', **kwargs):
    """Send document using ``send_file`` function.

    :param uri: Universal resource identifier of the document.
    :param mode: Mode for opening file when it needs to be streamed.
    :param kwargs: Additional arguments directly passed to ``send_file``.
    """
    if document.uri.startswith('http://') or \
            document.uri.startswith('https://'):
        return redirect(document.uri)

    # FIXME create better streaming support
    file_ = StringIO(document.open(mode).read())
    file_.seek(0)
    kwargs.setdefault('mimetype', 'application/octet-stream')
    return send_file(file_, **kwargs)
