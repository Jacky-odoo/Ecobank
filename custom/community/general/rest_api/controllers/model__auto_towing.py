# -*- coding: utf-8 -*-
from main import *

_logger = logging.getLogger(__name__)
from .commons import *

OUT__auto_towing__read_all__SUCCESS_CODE = 200
OUT__auto_towing__read_all__JSON = MODEL_AUTO_TOWING
OUT__auto_towing__read_one__SUCCESS_CODE = 200
OUT__auto_towing__read_one__JSON = MODEL_AUTO_TOWING

DEFAULTS__auto_towing__create_one__JSON = {}
OUT__auto_towing__create_one__SUCCESS_CODE = 200
OUT__auto_towing__create_one__JSON = ('id',)
OUT__auto_towing__update_one__SUCCESS_CODE = 200
OUT__auto_towing__delete_one__SUCCESS_CODE = 200
OUT__auto_towing__call_method__SUCCESS_CODE = 200
class ControllerREST(http.Controller):
    
    # Read all (with optional filters, offset, limit, order):
    @http.route('/api/auto.towing', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__auto_towing__GET(self, filters=None, offset=None, order=None, limit=None):
        return wrap__resource__read_all(
            modelname = 'auto.towing',
            default_domain = [],
            success_code = OUT__auto_towing__read_all__SUCCESS_CODE,
            OUT_fields = OUT__auto_towing__read_all__JSON
        )
    
    # Read one:
    @http.route('/api/auto.towing/<id>', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__auto_towing__id_GET(self, id):
        return wrap__resource__read_one(
            modelname = 'auto.towing',
            id = id,
            success_code = OUT__auto_towing__read_one__SUCCESS_CODE,
            OUT_fields = OUT__auto_towing__read_one__JSON
        )
    
    # Create one:
    @http.route('/api/auto.towing', methods=['POST'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__auto_towing__POST(self):
        return wrap__resource__create_one(
            modelname = 'auto.towing',
            default_vals = DEFAULTS__auto_towing__create_one__JSON,
            success_code = OUT__auto_towing__create_one__SUCCESS_CODE,
            OUT_fields = OUT__auto_towing__create_one__JSON
        )
    
    # Update one:
    @http.route('/api/auto.towing/<id>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__auto_towing__id_PUT(self, id):
        return wrap__resource__update_one(
            modelname = 'auto.towing',
            id = id,
            success_code = OUT__auto_towing__update_one__SUCCESS_CODE
        )
    

    
    # Call method (with optional parameters):
    @http.route('/api/auto.towing/<id>/<method>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__auto_towing__id__method_PUT(self, id, method):
        return wrap__resource__call_method(
            modelname = 'auto.towing',
            id = id,
            method = method,
            success_code = OUT__auto_towing__call_method__SUCCESS_CODE
        )
    
