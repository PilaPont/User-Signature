__author__ = 'mkz'

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"
    _description = "User Signature"

    signature_image = fields.Binary(string="Signature Image")
