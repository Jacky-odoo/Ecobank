# -*- coding: utf-8 -*-
# Part of Byte. See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class TestXMLRPC(common.HttpCase):
    at_install = False
    post_install = True

    def test_01_xmlrpc_login(self):
        """ Try to login on the common service. """
        db_name = common.get_db_name()
        uid = self.xmlrpc_common.login(db_name, 'admin', 'admin')
        self.assertEqual(uid, 1)

    def test_xmlrpc_ir_model_search(self):
        """ Try a search on the object service. """
        o = self.xmlrpc_object
        db_name = common.get_db_name()
        ids = o.execute(db_name, 1, 'admin', 'ir.model', 'search', [])
        self.assertIsInstance(ids, list)
        ids = o.execute(db_name, 1, 'admin', 'ir.model', 'search', [], {})
        self.assertIsInstance(ids, list)
