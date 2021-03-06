# -*- coding: utf-8 -*-
from main import *

_logger = logging.getLogger(__name__)
from .commons import *

OUT__auto_vehicle_spare_part__read_all__SUCCESS_CODE = 200
OUT__auto_vehicle_spare_part__read_all__JSON = MODEL_AUTO_VEHICLE_SPARE_PART
OUT__auto_vehicle_spare_part__read_one__SUCCESS_CODE = 200
OUT__auto_vehicle_spare_part__read_one__JSON = MODEL_AUTO_VEHICLE_SPARE_PART

DEFAULTS__auto_vehicle_spare_part__create_one__JSON = {}
OUT__auto_vehicle_spare_part__create_one__SUCCESS_CODE = 200
OUT__auto_vehicle_spare_part__create_one__JSON = ('id',)
OUT__auto_vehicle_spare_part__update_one__SUCCESS_CODE = 200
OUT__auto_vehicle_spare_part__delete_one__SUCCESS_CODE = 200
OUT__auto_vehicle_spare_part__call_method__SUCCESS_CODE = 200
class ControllerREST(http.Controller):
    
    # Read all (with optional filters, offset, limit, order):
    @http.route('/api/auto.vehicle.spare.part', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__auto_vehicle_spare_part__GET(self, filters=None, offset=None, order=None, limit=None):
        return wrap__resource__read_all(
            modelname = 'auto.vehicle.spare.part',
            default_domain = [],
            success_code = OUT__auto_vehicle_spare_part__read_all__SUCCESS_CODE,
            OUT_fields = OUT__auto_vehicle_spare_part__read_all__JSON
        )
    
    # Read one:
    @http.route('/api/auto.vehicle.spare.part/<id>', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__auto_vehicle_spare_part__id_GET(self, id):
        return wrap__resource__read_one(
            modelname = 'auto.vehicle.spare.part',
            id = id,
            success_code = OUT__auto_vehicle_spare_part__read_one__SUCCESS_CODE,
            OUT_fields = OUT__auto_vehicle_spare_part__read_one__JSON
        )
    
    # Create one:
    @http.route('/api/auto.vehicle.spare.part', methods=['POST'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__auto_vehicle_spare_part__POST(self):
        return wrap__resource__create_one(
            modelname = 'auto.vehicle.spare.part',
            default_vals = DEFAULTS__auto_vehicle_spare_part__create_one__JSON,
            success_code = OUT__auto_vehicle_spare_part__create_one__SUCCESS_CODE,
            OUT_fields = OUT__auto_vehicle_spare_part__create_one__JSON
        )
    
    # Update one:
    @http.route('/api/auto.vehicle.spare.part/<id>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__auto_vehicle_spare_part__id_PUT(self, id):
        return wrap__resource__update_one(
            modelname = 'auto.vehicle.spare.part',
            id = id,
            success_code = OUT__auto_vehicle_spare_part__update_one__SUCCESS_CODE
        )

    # Call method (with optional parameters):
    @http.route('/api/auto.vehicle.spare.part/<id>/<method>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__auto_vehicle_spare_part__id__method_PUT(self, id, method):
        return wrap__resource__call_method(
            modelname = 'auto.vehicle.spare.part',
            id = id,
            method = method,
            success_code = OUT__auto_vehicle_spare_part__call_method__SUCCESS_CODE
        )
    
