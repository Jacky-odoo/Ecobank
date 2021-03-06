# -*- coding: utf-8 -*- jpW9?WK.WG>.kYQ6
import functools
import hashlib
import logging
import os
from ast import literal_eval
try:
    import simplejson as json
except ImportError:
    import json

import werkzeug.wrappers

import odoo
from odoo import http, SUPERUSER_ID
from odoo.http import request, OpenERPSession
from odoo.modules.registry import RegistryManager
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

_logger = logging.getLogger(__name__)


def get_fields_values_from_model(modelname, domain, fields_list, offset=0, limit=None, order=None):
    cr, uid, context = request.cr, request.session.uid, request.context
    # cr._cnx.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)

    records = request.env[modelname].sudo().search(domain, offset=offset, limit=limit, order=order)
    if not records:
        return {}
    result = []
    for record in records:
        result += [get_fields_values_from_one_record(record, fields_list)]
    
    return result
    
def get_fields_values_from_one_record(record, fields_list):
    result = {}
    for field in fields_list:
        if type(field) == str:
            val = record[field]
            # If many2one _plane_ field
            try:
                val = val.id
            except:
                pass
            
            result[field] = val  if (val or '0' in str(val))  else None
        else:
            # Sample for One2many field: ('bank_ids', [('id', 'acc_number', 'bank_bic')])
            f_name, f_list = field[0], field[1]
            
            if type(f_list) == list:
                # Many (list of) records
                f_list = f_list[0]
                result[f_name] = []
                recs = record[f_name]
                for rec in recs:
                    result[f_name] += [get_fields_values_from_one_record(rec, f_list)]
            else:
                # One record
                rec = record[f_name]
                # protection against only one item without a comma
                if type(f_list) == str:
                    f_list = (f_list,)
                result[f_name] = get_fields_values_from_one_record(rec, f_list)
            
    return result

def convert_values_from_jdata_to_vals(modelname, jdata, creating=True):
    cr, uid, context = request.cr, request.session.uid, request.context
    Model = request.registry.get(modelname)
    
    x2m_fields = [f  for f in jdata  if type(jdata[f])==list]
    f_props = Model.fields_get(cr, uid, x2m_fields, context=context)
    
    vals = {}
    for field in jdata:
        val = jdata[field]
        if type(val) != list:
            vals[field] = val
        else:
            # x2many
            #
            # Sample for One2many field:
            # 'bank_ids': [{'acc_number': '12345', 'bank_bic': '6789'}, {'acc_number': '54321', 'bank_bic': '9876'}]
            vals[field] = []
            field_type = f_props[field]['type']
            # if updating of 'many2many'
            if (not creating) and (field_type == 'many2many'):
                # unlink all previous 'ids'
                vals[field].append((5,))
            
            for jrec in val:
                rec = {}
                for f in jrec:
                    rec[f] = jrec[f]
                
                if field_type == 'one2many':
                    if creating:
                        vals[field].append((0, 0, rec))
                    else:
                        if 'id' in rec:
                            id = rec['id']
                            del rec['id']
                            if len(rec):
                                # update record
                                vals[field].append((1, id, rec))
                            else:
                                # remove record
                                vals[field].append((2, id))
                        else:
                            # create record
                            vals[field].append((0, 0, rec))
                
                elif field_type == 'many2many':
                    # link current existing 'id'
                    vals[field].append((4, rec['id']))
    return vals

def create_object(modelname, vals):
    cr, uid, context = request.cr, request.session.uid, request.context
   # cr._cnx.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
    Model = request.registry.get(modelname)
    return Model.create(cr, uid, vals, context=context)

def update_object(modelname, obj_id, vals):
    cr, uid, context = request.cr, request.session.uid, request.context
    # cr._cnx.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
    Model = request.registry.get(modelname)
    return Model.write(cr, uid, [obj_id], vals, context=context)

def delete_object(modelname, obj_id):
    cr, uid, context = request.cr, request.session.uid, request.context
    # cr._cnx.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
    Model = request.registry.get(modelname)
    return Model.unlink(cr, uid, [obj_id], context=context)

def call_method_of_object(modelname, obj_id, method, jdata):
    cr, uid, context = request.cr, request.session.uid, request.context
    # cr._cnx.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
    Model = request.registry.get(modelname)
    # Validate method of model
    Method_of_model = getattr(Model, method, None)
    if callable(Method_of_model):
        # Execute method of object (with/without context)
        # (Not optimal code! But 'inspect.getargspec(Method_of_model)' - don't work properly here!)
        try:
            res = Method_of_model(cr, uid, [obj_id], context=context, **jdata)
        except:
            res = Method_of_model(cr, uid, [obj_id], **jdata)
    else:
        res = '__error__method_not_exist'
    return res


def wrap__resource__read_all(modelname, default_domain, success_code, OUT_fields):
    # Try convert http data into json:
    try:
        jdata = request.httprequest.headers
    except:
        jdata = {}
    # Default filter
    domain = default_domain or []
    # Get additional parameters
    if 'filters' in jdata:
        domain += literal_eval(jdata['filters'])
    if 'offset' in jdata:
        offset = int(jdata['offset'])
    else:
        offset = 0
    if 'limit' in jdata:
        limit = int(jdata['limit'])
    else:
        limit = None
    if 'order' in jdata:
        order = jdata['order']
    else:
        order = None
    # protection against only one item without a comma
    if type(OUT_fields) == str:
        OUT_fields = (OUT_fields,)
    # Reading object's data:
    Objects_Data = get_fields_values_from_model(
        modelname=modelname,
        domain=domain,
        offset=offset,
        limit=limit,
        order=order,
        fields_list=OUT_fields
    )
    return successful_response(status=success_code,
                               dict_data={
                                    'count': len(Objects_Data),
                                    'results': Objects_Data,
                                })

def wrap__resource__read_one(modelname, id, success_code, OUT_fields):
    # Default search field
    search_field = 'id'
    search_field_type = 'integer'
    # Try convert http data into json:
    try:
        jdata = json.loads(request.httprequest.stream.read())
        # Is there a search field?
        if jdata.get('search_field'):
            search_field = jdata['search_field']
            # Get search field type:
            cr, uid, context = request.cr, request.session.uid, request.context
            Model = request.registry.get(modelname)
            search_field_type = Model.fields_get(cr, uid, [search_field], context=context)[search_field]['type']
    except:
        pass
    # ??heck id
    obj_id = None
    if search_field_type == 'integer':
        try: obj_id = int(id)
        except: pass
    else:
        obj_id = id
    if not obj_id:
        return error_response_400__invalid_object_id()
    # protection against only one item without a comma
    if type(OUT_fields) == str:
        OUT_fields = (OUT_fields,)
    # Reading object's data:
    Object_Data = get_fields_values_from_model(
        modelname = modelname,
        domain = [(search_field, '=', obj_id)],
        fields_list = OUT_fields
    )
    if Object_Data:
        return successful_response(success_code, Object_Data[0])
    else:
        return error_response_404__not_found_object_in_server()

def wrap__resource__create_one(modelname, default_vals, success_code, OUT_fields=('id',)):
    # Convert http data into json:
    try:
        jdata = request.httprequest.headers
    except:
        jdata = {}
    if jdata:
        data = literal_eval(jdata['data'])
        # Convert json data into Server vals:
        vals = convert_values_from_jdata_to_vals(modelname, data)
        # Set default fields:
        if default_vals:
            vals.update(default_vals)
        # Try create new object
        try:
            new_id = create_object(modelname, vals)
            server_error = ''
        except Exception, e:
            new_id = None
            server_error = e.message
        if new_id:
            # protection against only one item without a comma
            if type(OUT_fields) == str:
                OUT_fields = (OUT_fields,)
            response_json = get_fields_values_from_model(
                modelname = modelname,
                domain = [('id', '=', new_id)],
                fields_list = OUT_fields
            )[0]
            return successful_response(success_code, response_json)
        else:
            return error_response_409__not_created_object_in_server(server_error)

def wrap__resource__update_one(modelname, id, success_code):
    # ??heck id
    obj_id = None
    try:
        obj_id = int(id)
    except:
        pass
    if not obj_id:
        return error_response_400__invalid_object_id()
    # Convert http data into json:
    jdata = request.httprequest.headers
    if jdata:
        data = literal_eval(jdata['data'])
        # Convert json data into Server vals:
        vals = convert_values_from_jdata_to_vals(modelname, data, creating=False)
        # Try update the object
        try:
            res = update_object(modelname, obj_id, vals)
            server_error = ''
        except Exception, e:
            res = None
            server_error = e.message
        if res:
            return successful_response(success_code, {})
        else:
            return error_response_409__not_updated_object_in_server(server_error)

def wrap__resource__delete_one(modelname, id, success_code):
    # ??heck id
    obj_id = None
    try:
        obj_id = int(id)
    except:
        pass
    if not obj_id:
        return error_response_400__invalid_object_id()
    # Try delete the object
    try:
        res = delete_object(modelname, obj_id)
        server_error = ''
    except Exception, e:
        res = None
        server_error = e.message
    if res:
        return successful_response(success_code, {})
    else:
        return error_response_409__not_deleted_object_in_server(server_error)

def wrap__resource__call_method(modelname, id, method, success_code):
    # ??heck id
    obj_id = None
    try:
        obj_id = int(id)
    except:
        pass
    if not obj_id:
        return error_response_400__invalid_object_id()
    # Try convert http data into json:
    try:
        jdata = json.loads(request.httprequest.stream.read())
    except:
        jdata = {}
    # Try call method of object
    _logger.info("Try call method of object: modelname == %s; obj_id == %s; method == %s; len(jdata) == %s" \
                    % (modelname, obj_id, method, len(jdata)))
    _logger.debug("jdata == %s" % jdata)
    try:
        res = call_method_of_object(modelname, obj_id, method, jdata)
        server_error = ''
    except Exception, e:
        res = None
        server_error = e.message
    if res:
        if res == '__error__method_not_exist':
            return error_response_501__method_not_exist_in_server()
        else:
            return successful_response(success_code, json.dumps(res))
    else:
        return error_response_409__not_called_method_in_server(server_error)


def check_permissions(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        _logger.info("Check permissions...")
        
        # Get access token from http header
        access_token = request.httprequest.headers.get('access_token')
        if not access_token:
            error_descrip = "No access token was provided in request header!"
            error = 'no_access_token'
            _logger.error(error_descrip)
            return error_response(400, error, error_descrip)
        
        # Validate access token
        access_token_data = token_store.fetch_by_access_token(access_token)
        if not access_token_data:
            return error_response_401__invalid_token()
        
        # Set session UID from current access token
        request.session.uid = access_token_data['user_id']
        
        # The code, following the decorator
        return func(self, *args, **kwargs)
    return wrapper


def successful_response(status, dict_data):
    return werkzeug.wrappers.Response(
        status = status,
        content_type = 'application/json; charset=utf-8',
        #headers = None,
        response = json.dumps(dict_data),
    )

def error_response(status, error, error_descrip):
    return werkzeug.wrappers.Response(
        #status = status,
        content_type = 'application/json; charset=utf-8',
        #headers = None,
        response = json.dumps({
            'code': status,
            'error': error,
            'error_descrip': error_descrip,
        }),
    )

def error_response_400__invalid_object_id():
    error_descrip = "Invalid object 'id'!"
    error = 'invalid_object_id'
    _logger.error(error_descrip)
    return error_response(400, error, error_descrip)

def error_response_401__invalid_token():
    error_descrip = "Token is expired or invalid!"
    error = 'invalid_token'
    _logger.error(error_descrip)
    return error_response(401, error, error_descrip)

def error_response_404__not_found_object_in_server():
    error_descrip = "Not found object(s) in Server!"
    error = 'not_found_object_in_server'
    _logger.error(error_descrip)
    return error_response(404, error, error_descrip)

def error_response_409__not_created_object_in_server(server_error):
    error_descrip = "Not created object in Server! ERROR: %s" % server_error
    error = 'not_created_object_in_server'
    _logger.error(error_descrip)
    return error_response(409, error, error_descrip)

def error_response_409__not_updated_object_in_server(server_error):
    error_descrip = "Not updated object in Server! ERROR: %s" % server_error
    error = 'not_updated_object_in_server'
    _logger.error(error_descrip)
    return error_response(409, error, error_descrip)

def error_response_409__not_deleted_object_in_server(server_error):
    error_descrip = "Not deleted object in Server! ERROR: %s" % server_error
    error = 'not_deleted_object_in_server'
    _logger.error(error_descrip)
    return error_response(409, error, error_descrip)

def error_response_409__not_called_method_in_server(server_error):
    error_descrip = "Not called method in Server! ERROR: %s" % server_error
    error = 'not_called_method_in_server'
    _logger.error(error_descrip)
    return error_response(409, error, error_descrip)

def error_response_501__method_not_exist_in_server():
    error_descrip = "Method not exist in Server!"
    error = 'method_not_exist_in_server'
    _logger.error(error_descrip)
    return error_response(501, error, error_descrip)


def generate_token(length=40):
    random_data = os.urandom(100)
    hash_gen = hashlib.new('sha512')
    hash_gen.update(random_data)
    return hash_gen.hexdigest()[:length]


# Read OAuth2 constants and setup Redis token store:
config = odoo.tools.config

access_token_expires_in = config.get('oauth2_access_token_expires_in', 600000)
refresh_token_expires_in = config.get('oauth2_refresh_token_expires_in', 600000)
redis_host = config.get('redis_host', 'localhost')
redis_port = config.get('redis_port', 6379)
redis_db = config.get('redis_db', 0)
redis_password = config.get('redis_password')
if redis_password in ('None', 'False'):
    redis_password = None
# Setup Redis token store and resources:
if redis_host and redis_port:
    import redisdb
    token_store = redisdb.RedisTokenStore(
                            host = redis_host,
                            port = redis_port,
                            db = redis_db,
                            password = redis_password)
    import resources

    _logger.info("INFO: rest api successfully loaded!")
    print "INFO: rest api successfully loaded!"
else:
    _logger.warning("WARNING: It's necessary to RESTART server after the installation of 'rest_api' module!")
    print "WARNING: It's necessary to RESTART server after the installation of 'rest_api' module!"

