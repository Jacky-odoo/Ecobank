# -*- coding: utf-8 -*-
from main import *

_logger = logging.getLogger(__name__)
from .commons import *

OUT__auto_vehicle_spare_part_purchase__read_all__SUCCESS_CODE = 200
OUT__auto_vehicle_spare_part_purchase__read_all__JSON = MODEL_AUTO_VEHICLE_SPARE_PART_PURCHASE
OUT__auto_vehicle_spare_part_purchase__read_one__SUCCESS_CODE = 200
OUT__auto_vehicle_spare_part_purchase__read_one__JSON = MODEL_AUTO_VEHICLE_SPARE_PART_PURCHASE

DEFAULTS__auto_vehicle_spare_part_purchase__create_one__JSON = {}
OUT__auto_vehicle_spare_part_purchase__create_one__SUCCESS_CODE = 200
OUT__auto_vehicle_spare_part_purchase__create_one__JSON = ('id',)
OUT__auto_vehicle_spare_part_purchase__update_one__SUCCESS_CODE = 200
OUT__auto_vehicle_spare_part_purchase__delete_one__SUCCESS_CODE = 200
OUT__auto_vehicle_spare_part_purchase__call_method__SUCCESS_CODE = 200
class ControllerREST(http.Controller):
    
    # Read all (with optional filters, offset, limit, order):
    @http.route('/api/auto.spare.part.purchase', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__auto_vehicle_spare_part_purchase__GET(self, filters=None, offset=None, order=None, limit=None):
        return wrap__resource__read_all(
            modelname = 'auto.spare.part.purchase',
            default_domain = [],
            success_code = OUT__auto_vehicle_spare_part_purchase__read_all__SUCCESS_CODE,
            OUT_fields = OUT__auto_vehicle_spare_part_purchase__read_all__JSON
        )
    
    # Read one:
    @http.route('/api/auto.spare.part.purchase/<id>', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__auto_vehicle_spare_part_purchase__id_GET(self, id):
        return wrap__resource__read_one(
            modelname = 'auto.spare.part.purchase',
            id = id,
            success_code = OUT__auto_vehicle_spare_part_purchase__read_one__SUCCESS_CODE,
            OUT_fields = OUT__auto_vehicle_spare_part_purchase__read_one__JSON
        )
    
    # Create one:
    @http.route('/api/auto.spare.part.purchase', methods=['POST'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__auto_vehicle_spare_part_purchase__POST(self):
        return wrap__resource__create_one(
            modelname = 'auto.spare.part.purchase',
            default_vals = DEFAULTS__auto_vehicle_spare_part_purchase__create_one__JSON,
            success_code = OUT__auto_vehicle_spare_part_purchase__create_one__SUCCESS_CODE,
            OUT_fields = OUT__auto_vehicle_spare_part_purchase__create_one__JSON
        )
    
    # Update one:
    @http.route('/api/auto.spare.part.purchase/<id>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__auto_vehicle_spare_part_purchase__id_PUT(self, id):
        return wrap__resource__update_one(
            modelname = 'auto.spare.part.purchase',
            id = id,
            success_code = OUT__auto_vehicle_spare_part_purchase__update_one__SUCCESS_CODE
        )
    

    
    # Call method (with optional parameters):
    @http.route('/api/auto.spare.part.purchase/<id>/<method>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__auto_vehicle_spare_part_purchase__id__method_PUT(self, id, method):
        return wrap__resource__call_method(
            modelname = 'auto.spare.part.purchase',
            id = id,
            method = method,
            success_code = OUT__auto_vehicle_spare_part_purchase__call_method__SUCCESS_CODE
        )
