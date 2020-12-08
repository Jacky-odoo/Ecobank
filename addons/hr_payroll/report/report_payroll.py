import time
from datetime import datetime
from odoo.osv import osv
from odoo.report import report_sxw
from odoo.tools import amount_to_text_en


class PayrollReport(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(PayrollReport, self).__init__(cr, uid, name,
                                                    context=context)

        self.localcontext.update({
            'time': time,
            'get_month': self.get_month,
            'get_detail': self.get_detail,
            'get_total_net': self.get_total_net,
            'get_total_basic': self.get_total_basic,
            'get_total_gross': self.get_total_gross,
            'get_total_nassit': self.get_total_nassit,
            'get_total_nassitte': self.get_total_nassitte,
            'get_total_paye': self.get_total_paye,
            'get_total_ded':  self.get_total_ded,
            'get_total_allowances': self.get_total_allowances,

        })
        self.context = context

    def get_month(self, run_id):
        date = run_id.date_payment
        date_dt = datetime.strptime(date, '%Y-%m-%d')
        return "STAFF PAYROLL FOR " +date_dt.strftime("%B").upper()+", "+str(date_dt.year)

    def convert(self, amount, cur):
        return amount_to_text_en.amount_to_text(amount, 'en', cur)

    def get_detail(self, slip_ids):
        result = []
        for s in slip_ids:
            gross = s.line_ids.filtered(lambda r: r.code == "GROSS").total
            basic = s.line_ids.filtered(lambda r: r.code == "BASIC").total
            result.append({
                'name': s.employee_id.name,
                'basic': basic,
                'allowances': gross - basic,
                'gross': gross,
                'nassit': basic*0.05,
                'nassitte': basic*0.10,
                'paye': s.line_ids.filtered(lambda r: r.code == "PAYE").total,
                'ded': s.line_ids.filtered(lambda r: r.code == "TOTALDED").total,
                'net': s.line_ids.filtered(lambda r: r.code == "NET").total,
            })

        return result

    def get_total_net(self, slip_ids):
        total = 0
        for s in slip_ids:
            total += s.line_ids.filtered(lambda r: r.code == "NET").total
        return total

    def get_total_basic(self, slip_ids):
        total = 0
        for s in slip_ids:
            total += s.line_ids.filtered(lambda r: r.code == "BASIC").total
        return total

    def get_total_gross(self, slip_ids):
        total = 0
        for s in slip_ids:
            total += s.line_ids.filtered(lambda r: r.code == "GROSS").total
        return total

    def get_total_nassit(self, slip_ids):
        total = 0
        for s in slip_ids:
            total += s.line_ids.filtered(lambda r: r.code == "BASIC").total*0.05
        return total

    def get_total_nassitte(self, slip_ids):
        total = 0
        for s in slip_ids:
            total += s.line_ids.filtered(lambda r: r.code == "BASIC").total*0.10
        return total

    def get_total_paye(self, slip_ids):
        total = 0
        for s in slip_ids:
            total += s.line_ids.filtered(lambda r: r.code == "PAYE").total
        return total

    def get_total_ded(self, slip_ids):
        total = 0
        for s in slip_ids:
            total += s.line_ids.filtered(lambda r: r.code == "TOTALDED").total
        return total

    def get_total_allowances(self, slip_ids):
        return self.get_total_gross(slip_ids) - self.get_total_basic(slip_ids)


class WrappedReportPayroll(osv.AbstractModel):
    _name = 'report.hr_payroll.payroll_report_template'
    _inherit = 'report.abstract_report'
    _template = 'hr_payroll.payroll_report_template'
    _wrapped_report_class = PayrollReport
