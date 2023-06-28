from odoo import api, models, _
from odoo.exceptions import UserError


class Invoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_draft(self):
        super().action_invoice_draft()
        for inv in self:
            if not inv.env.context.get(
                "rc_set_to_draft"
            ) and inv.rc_purchase_invoice_id.state in ["draft", "cancel"]:
                raise UserError(
                    _(
                        "Vendor invoice that has generated this self invoice isn't "
                        "validated. "
                        "Validate vendor invoice before."
                    )
                )
        return True
