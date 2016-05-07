# -*- coding: utf-8 -*-
# © 2014 Compassion CH - Cyril Sester <csester@compassion.ch>
# © 2014 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2015-2016 Akretion - Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class AccountPaymentLine(models.Model):
    _inherit = 'account.payment.line'

    mandate_id = fields.Many2one(
        comodel_name='account.banking.mandate', string='Direct Debit Mandate',
        domain=[('state', '=', 'valid')])

    @api.multi
    @api.constrains('mandate_id', 'partner_bank_id')
    def _check_mandate_bank_link(self):
        for pline in self:
            if (pline.mandate_id and pline.partner_bank_id and
                    pline.mandate_id.partner_bank_id !=
                    pline.partner_bank_id):
                raise ValidationError(_(
                    "The payment line number %s has the bank account "
                    "'%s' which is not attached to the mandate '%s' (this "
                    "mandate is attached to the bank account '%s').") %
                    (pline.name,
                     pline.partner_bank_id.acc_number,
                     pline.mandate_id.unique_mandate_reference,
                     pline.mandate_id.partner_bank_id.acc_number))

#    @api.multi
#    def check_payment_line(self):
# TODO : i would like to block here is mandate is missing...
# but how do you know it's required ? => create option on payment order ?