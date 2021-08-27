import io
import base64
from PIL import Image
from math import isclose

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = "res.users"
    _description = "User Signature"

    signature_image = fields.Binary(string="Signature Image",
                                    help="Upload user signature image. Please pay attention, the allowable aspect ratio"
                                         " of signature image is 'one', with a maximum tolerance of 0.05!")

    @api.model
    def create(self, values):
        signature_image = values.get('signature_image')
        if signature_image:
            self._check_signature_dimensions(signature_image)
        result = super(ResUsers, self).create(values)
        return result

    def write(self, values):
        for user in self:
            signature_image = values.get('signature_image')
            if signature_image:
                user._check_signature_dimensions(signature_image)
        result = super(ResUsers, self).write(values)
        return result

    @staticmethod
    def _check_signature_dimensions(signature_image):
        image_decoded = base64.decodebytes(signature_image.encode('utf-8'))
        signature_image_string = io.BytesIO(image_decoded)
        width, height = Image.open(signature_image_string).size
        if not isclose(width, height, rel_tol=0.05):
            raise UserError(
                _("The allowable aspect ratio of signature image is 'one' with a maximum tolerance of 0.05!"))
