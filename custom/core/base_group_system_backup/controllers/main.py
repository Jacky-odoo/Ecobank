# -*- coding: utf-8 -*-
import datetime
import odoo
from odoo import api, SUPERUSER_ID
from odoo import http
from odoo.http import request

from odoo.http import request, content_disposition


import werkzeug


import logging
_logger = logging.getLogger(__name__)

class BackupServer(http.Controller):

    @http.route('/web/group_system_backup', type='http', auth="user")
    def backup(self, backup_format='zip'):
        backup_db = request.session.db
        ts = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        filename = "%s_%s.%s" % (backup_db, ts, backup_format)
        headers = [
            ('Content-Type', 'application/octet-stream; charset=binary'),
            ('Content-Disposition', content_disposition(filename)),
        ]
        dump_stream = odoo.service.db.dump_db(backup_db, None, backup_format)
        response = werkzeug.wrappers.Response(dump_stream, headers=headers, direct_passthrough=True)
        return response

