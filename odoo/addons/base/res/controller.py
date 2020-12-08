# -*- coding: utf-8 -*-
import logging
try:
    import simplejson as json
except ImportError:
    import json

import werkzeug.wrappers

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)
OUT__auth_gettokens__SUCCESS_CODE = 200
OUT__auth_gettokens__ERROR_CODE = 400


def get_nassit(basic_pay, employee_type, age, nassit_contribution=True):
    nassit = 0.0
    nassittee = 0.0
    if employee_type == 'local':
        if age >= 60:
            return {'Nassit': nassit, 'Nassittee': nassittee}
        if not nassit_contribution:
            return {'Nassit': nassit, 'Nassittee': nassittee}
        else:
            nassit += basic_pay * 0.05
            nassittee += basic_pay * 0.10
    return {'Nassit': nassit, 'Nassittee': nassittee}


def calculate_sl_tax(basic_pay, gross, age, employee_type, non_tax_earning, nassit_contribution=True):
    nassits = get_nassit(basic_pay, employee_type, age, nassit_contribution)
    total_paye = 0.0
    if employee_type == 'foreign':
        total_paye += basic_pay * 0.05
    else:
        tax_income = gross - nassits['Nassit'] - non_tax_earning
        if tax_income <= 500000:
            return {'Paye': total_paye, 'Nassit': nassits['Nassit'], 'Nassittee': nassits['Nassittee']}
        if 500000 < tax_income <= 1000000:
            total_paye += (tax_income - 500000) * 0.15
            return {'Paye': total_paye, 'Nassit': nassits['Nassit'], 'Nassittee': nassits['Nassittee']}
        if 1000000 < tax_income <= 1500000:
            total_paye += (tax_income - 1000000) * 0.20 + 75000
            return {'Paye': total_paye, 'Nassit': nassits['Nassit'], 'Nassittee': nassits['Nassittee']}
        if 1500000 < tax_income <= 2000000:
            total_paye += (tax_income - 1500000) * 0.25 + 75000 + 100000
            return {'Paye': total_paye, 'Nassit': nassits['Nassit'], 'Nassittee': nassits['Nassittee']}
        if 2000000 < tax_income <= 2000000000:
            total_paye += (tax_income - 2000000) * 0.30 + 75000 + 100000 + 125000
    return {'Paye': total_paye, 'Nassit': nassits['Nassit'], 'Nassittee': nassits['Nassittee']}


def calculate_gmb_tax(gross, non_tax_earning):
    total_paye = 0.0
    tax_income = gross - non_tax_earning
    if tax_income <= 2000:
        return {'Monthly Income Tax': total_paye, 'Yearly Income Tax': total_paye*12}
    if 2000 < tax_income <= 2833.3:
        total_paye += (tax_income - 833.3) * 0.05
        return {'Monthly Income Tax': total_paye, 'Yearly Income Tax': total_paye*12}
    if 2833.3 < tax_income <= 3666.6:
        total_paye += (tax_income - 2833.3) * 0.10 + 41.67
        return {'Monthly Income Tax': total_paye, 'Yearly Income Tax': total_paye*12}
    if 3666.6 < tax_income <= 4499.9:
        total_paye += (tax_income - 3666.6) * 0.15 + 41.67 + 83.33
        return {'Monthly Income Tax': total_paye, 'Yearly Income Tax': total_paye*12}
    if 4499.9 < tax_income <= 5333.2:
        total_paye += (tax_income - 4499.9) * 0.20 + 41.67 + 83.33 + 124.99
        return {'Monthly Income Tax': total_paye, 'Yearly Income Tax': total_paye*12}
    if 5333.2 < tax_income <= 2000000000:
        total_paye += (tax_income - 5333.2) * 0.25 + 41.67 + 83.33 + 124.99 + 166.67
    return {'Monthly Income Tax': total_paye, 'Yearly Income Tax': total_paye*12}


def check_values(value):
    return float(value) > 0.0 and type(value) == float


class ControllerREST(http.Controller):
    
    @http.route('/api/tax', methods=['POST'], type='http', auth='none', csrf=False)
    def api_tax_calculation(self):
        # Convert http data into json:
        _logger.info("API Was reached successfully")
        try:
            jdata = json.loads(request.httprequest.stream.read())
        except:
            jdata = {}
        if 'country' in jdata:
            country = jdata.get('country')
            if country == 'sl':
                """
                fields required for sl
                basic_pay, gross, age, employee_type, non_tax_earning, nassit_contribution=True
                """
                try:
                    basic_pay = jdata.get('basic_pay')
                    assert float(basic_pay)
                except :
                    return werkzeug.wrappers.Response(
                        status=OUT__auth_gettokens__ERROR_CODE,
                        content_type='application/json; charset=utf-8',
                        headers=[('Cache-Control', 'no-store'),
                                 ('Pragma', 'no-cache')],
                        response=json.dumps({'error': 'Required Parameter basic_pay not found or not in the required type'}),)

                try:
                    gross = jdata.get('gross')
                    assert float(gross)
                except:
                    return werkzeug.wrappers.Response(
                        status=OUT__auth_gettokens__ERROR_CODE,
                        content_type='application/json; charset=utf-8',
                        headers=[('Cache-Control', 'no-store'),
                                 ('Pragma', 'no-cache')],
                        response=json.dumps({'error': 'Required Parameter gross not found or not in the required type'}),)

                try:
                    age = jdata.get('age')
                    assert int(age)
                except :
                    return werkzeug.wrappers.Response(
                        status=OUT__auth_gettokens__ERROR_CODE,
                        content_type='application/json; charset=utf-8',
                        headers=[('Cache-Control', 'no-store'),
                                 ('Pragma', 'no-cache')],
                        response=json.dumps({'error': 'Required Parameter age not found or not in the required type'}),)

                try:
                    employee_type = jdata.get('employee_type')
                    assert len(str(employee_type)) > 0
                except :
                    return werkzeug.wrappers.Response(
                        status=OUT__auth_gettokens__ERROR_CODE,
                        content_type='application/json; charset=utf-8',
                        headers=[('Cache-Control', 'no-store'),
                                 ('Pragma', 'no-cache')],
                        response=json.dumps({'error': 'Required Parameter employee_type not found or not in the required type'}),)

                try:
                    non_tax_earning = jdata.get('non_tax_earning')
                    assert float(non_tax_earning)
                except :
                    return werkzeug.wrappers.Response(
                        status=OUT__auth_gettokens__ERROR_CODE,
                        content_type='application/json; charset=utf-8',
                        headers=[('Cache-Control', 'no-store'),
                                 ('Pragma', 'no-cache')],
                        response=json.dumps({'error': 'Required Parameter non_tax_earning not found or not in the required type'}),)

                try:
                    nassit_contribution = jdata.get('nassit_contribution')
                    assert bool(nassit_contribution)
                except :
                    return werkzeug.wrappers.Response(
                        status=OUT__auth_gettokens__ERROR_CODE,
                        content_type='application/json; charset=utf-8',
                        headers=[('Cache-Control', 'no-store'),
                                 ('Pragma', 'no-cache')],
                        response=json.dumps({'error': 'Required Parameter nassit_contribution not found or not in the required type'}),)

                return werkzeug.wrappers.Response(
                    status=OUT__auth_gettokens__SUCCESS_CODE,
                    content_type='application/json; charset=utf-8',
                    headers=[('Cache-Control', 'no-store'),
                             ('Pragma', 'no-cache')],
                    response=json.dumps(calculate_sl_tax(float(basic_pay),
                                                         float(gross),
                                                         int(age),
                                                         str(employee_type),
                                                         float(non_tax_earning),
                                                         bool(nassit_contribution))),)
            if country == 'gmb':
                """
                calculate_gmb_tax(gross, non_tax_earning)
                fields required for sl
                gross, non_tax_earning
                """
                try:
                    gross = jdata.get('gross')
                    assert float(gross)
                    assert float(gross) > 0.0
                except :
                    return werkzeug.wrappers.Response(
                        status=OUT__auth_gettokens__ERROR_CODE,
                        content_type='application/json; charset=utf-8',
                        headers=[('Cache-Control', 'no-store'),
                                 ('Pragma', 'no-cache')],
                        response=json.dumps({'error': 'Required Parameter gross not found or not in the required type.'
                                                      ' Gross must be a float greater than 0.0'}),)

                try:
                    non_tax_earning = float(jdata.get('non_tax_earning'))
                    assert float(non_tax_earning) > 0.0
                except:
                    return werkzeug.wrappers.Response(
                        status=OUT__auth_gettokens__ERROR_CODE,
                        content_type='application/json; charset=utf-8',
                        headers=[('Cache-Control', 'no-store'),
                                 ('Pragma', 'no-cache')],
                        response=json.dumps({'error': 'Required Parameter non_tax_earning not found or not '
                                                      'in the required type. Value must be a float greater than 0.0'}),)

                return werkzeug.wrappers.Response(
                    status=OUT__auth_gettokens__SUCCESS_CODE,
                    content_type='application/json; charset=utf-8',
                    headers=[('Cache-Control', 'no-store'),
                             ('Pragma', 'no-cache')],
                    response=json.dumps(calculate_gmb_tax(gross, non_tax_earning)),)
            if country == 'ng':
                return werkzeug.wrappers.Response(
                    status=OUT__auth_gettokens__SUCCESS_CODE,
                    content_type='application/json; charset=utf-8',
                    headers=[('Cache-Control', 'no-store'),
                             ('Pragma', 'no-cache')],
                    response=json.dumps({'Result': "Api Not Yet Ready"}),)
            if country == 'sa':
                return werkzeug.wrappers.Response(
                    status=OUT__auth_gettokens__SUCCESS_CODE,
                    content_type='application/json; charset=utf-8',
                    headers=[('Cache-Control', 'no-store'),
                             ('Pragma', 'no-cache')],
                    response=json.dumps({'Result': "Api Not Yet Ready"}),)
            if country == 'lib':
                return werkzeug.wrappers.Response(
                    status=OUT__auth_gettokens__SUCCESS_CODE,
                    content_type='application/json; charset=utf-8',
                    headers=[('Cache-Control', 'no-store'),
                             ('Pragma', 'no-cache')],
                    response=json.dumps({'Result': "Api Not Yet Ready"}),)
        return werkzeug.wrappers.Response(
            status=OUT__auth_gettokens__SUCCESS_CODE,
            content_type='application/json; charset=utf-8',
            headers=[('Cache-Control', 'no-store'),
                     ('Pragma', 'no-cache')],
            response=json.dumps({'Result': "Api Not Yet Ready"}), )

