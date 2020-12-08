# -*- coding: utf-8 -*-
from main import *

_logger = logging.getLogger(__name__)
from .commons import *

OUT__auto_user__read_all__SUCCESS_CODE = 200
OUT__auto_user__read_all__JSON = MODEL_AUTO_USER
OUT__auto_user__read_one__SUCCESS_CODE = 200
OUT__auto_user__read_one__JSON = MODEL_AUTO_USER

DEFAULTS__auto_user__create_one__JSON = {}
OUT__auto_user__create_one__SUCCESS_CODE = 200
OUT__auto_user__create_one__JSON = ('id',)
OUT__auto_user__update_one__SUCCESS_CODE = 200
OUT__auto_user__delete_one__SUCCESS_CODE = 200
OUT__auto_user__call_method__SUCCESS_CODE = 200
class ControllerREST(http.Controller):
    
    # Read all (with optional filters, offset, limit, order):
    @http.route('/api/auto.user', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__auto_user__GET(self, filters=None, offset=None, order=None, limit=None):
        return wrap__resource__read_all(
            modelname = 'auto.user',
            default_domain = [],
            success_code = OUT__auto_user__read_all__SUCCESS_CODE,
            OUT_fields = OUT__auto_user__read_all__JSON
        )
    
    # Read one:
    @http.route('/api/auto.user/<id>', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__auto_user__id_GET(self, id):
        return wrap__resource__read_one(
            modelname = 'auto.user',
            id = id,
            success_code = OUT__auto_user__read_one__SUCCESS_CODE,
            OUT_fields = OUT__auto_user__read_one__JSON
        )
    
    # Create one:
    @http.route('/api/auto.user', methods=['POST'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__auto_user__POST(self):
        return wrap__resource__create_one(
            modelname = 'auto.user',
            default_vals = DEFAULTS__auto_user__create_one__JSON,
            success_code = OUT__auto_user__create_one__SUCCESS_CODE,
            OUT_fields = OUT__auto_user__create_one__JSON
        )
    
    # Update one:
    @http.route('/api/auto.user/<id>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__auto_user__id_PUT(self, id):
        return wrap__resource__update_one(
            modelname = 'auto.user',
            id = id,
            success_code = OUT__auto_user__update_one__SUCCESS_CODE
        )

    
    # Call method (with optional parameters):
    @http.route('/api/auto.user/<id>/<method>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__auto_user__id__method_PUT(self, id, method):
        return wrap__resource__call_method(
            modelname = 'auto.user',
            id = id,
            method = method,
            success_code = OUT__auto_user__call_method__SUCCESS_CODE
        )
    
