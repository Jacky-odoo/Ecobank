from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = 'res.company'

    checkin_time = fields.Char(string="Check in Time", default="8:30")
    checkout_time = fields.Char(string="Check out Time", default="17:30")

    @api.constrains('checkin_time', 'checkout_time')
    def check_attendance(self):
        for rec in self:
            if not (rec.checkin_time and rec.checkout_time):
                raise ValidationError("Please specify checkout and checkout time time")
            if len(str(rec.checkin_time)) > 5 or len(str(rec.checkout_time)) > 5:
                raise ValidationError("Incorrect checkin/checkout Time")
            try:
                i_hour = int(str(rec.checkin_time).split(':')[0])
                i_min = int(str(rec.checkin_time).split(':')[-1])
                o_hour = int(str(rec.checkout_time).split(':')[0])
                o_min = int(str(rec.checkout_time).split(':')[-1])
            except Exception:
                raise ValidationError("incorrect time format")
            if i_hour*60+i_min > o_hour*60+o_min:
                raise ValidationError("checkin time cannot be greater than checkout time")
            if i_hour > 23 or o_hour < 0:
                raise ValidationError("Invalid Checkin time")
            if i_min > 59 or o_hour < 0:
                raise ValidationError("Invalid Checkoin time")
            if o_hour > 23 or o_hour < 0:
                raise ValidationError("Invalid Checkout time")
            if o_min > 59 or o_hour < 0:
                raise ValidationError("Invalid Checkout time")




