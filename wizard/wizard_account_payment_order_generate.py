import logging
from collections import defaultdict
from odoo import models, api, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountPaymentGenerate(models.TransientModel):
    _name = 'wizard.account.payment.generate'
    _description = 'Create payment order from due dates tree view'

    def _set_default_mode(self):
        active_ids = self._context.get('active_ids')

        payment_method = False

        if active_ids and len(active_ids) > 0:
            lines = self.env['account.move.line'].browse(active_ids)
            for line in lines:
                payment_method = line.payment_method
                break
        if payment_method:
            domain = [('payment_method_id', '=', payment_method.id),
                      ('active', '=', True)]
        else:
            domain = [('active', '=', True)]

        records = self.env['account.payment.mode'].search(domain)
        if len(records) == 1:
            return records[0].id
        return False

    def _set_domain_journal(self):
        active_ids = self._context.get('active_ids')
        invoice_bank_id = False
        payment_method = False
        default_domain = [('type', '=', 'bank'),
                          ('bank_account_id', '!=', False)]
        if active_ids and len(active_ids) > 0:
            lines = self.env['account.move.line'].browse(active_ids)
            for line in lines:
                payment_method = line.payment_method
                invoice_bank_id = line.move_id.invoice_bank_id.id
                break
            # end for
        # end if

        if payment_method and payment_method.code and \
                payment_method.code == 'invoice_financing':
            search_domain = [
                ('type', '=', 'bank'),
                ('bank_account_id', '=', invoice_bank_id),
            ]
            records = self.env['account.journal'].search(
                search_domain,
                order='sequence asc',
                limit=1
            )
            if len(records) == 1:
                return search_domain
            else:
                return default_domain
            # end if
        else:
            return default_domain
        # end if

    # end _set_domain_journal

    def _set_default_journal(self):
        active_ids = self._context.get('active_ids')
        invoice_bank_id = False
        payment_method = False

        if active_ids and len(active_ids) > 0:
            lines = self.env['account.move.line'].browse(active_ids)
            for line in lines:
                payment_method = line.payment_method
                invoice_bank_id = line.move_id.invoice_bank_id.id
                break
            # end for
        # end if

        if payment_method and payment_method.code and \
                payment_method.code == 'invoice_financing':
            search_domain = [
                ('type', '=', 'bank'),
                ('bank_account_id', '=', invoice_bank_id),
            ]
            records = self.env['account.journal'].search(
                search_domain,
                order='sequence asc',
                limit=1
            )
            if len(records) == 1:
                return records[0].id
            else:
                return False
            # end if
        else:
            return False
        # end if

    # end _set_default_journal

    payment_mode_id = fields.Many2one(
        'account.payment.mode',
        string='Payment Mode',
        required=True,
        default=_set_default_mode
    )

    journal_id = fields.Many2one(
        'account.journal',
        string='Bank Journal',
        domain=_set_domain_journal,
        # domain=[('type', '=', 'bank'), ('bank_account_id', '!=', False)],
        deafult=_set_default_journal
    )

    description = fields.Char(string='Description')

    @api.onchange('payment_mode_id')
    def on_change_payment_mode(self):
        active_ids = self._context.get('active_ids')

        if active_ids and len(active_ids) > 0:
            lines = self.env['account.move.line'].browse(active_ids)
            self._raise_on_errors(lines)
            mode_ids = []
            # according to validation there is only one payment method
            # catch the first one
            for line in lines:
                payment_method = line.payment_method
                break
            # end for

            if payment_method:
                domain = [('payment_method_id', '=', payment_method.id),
                          ('active', '=', True)]
            else:
                domain = [('active', '=', True)]
            # end if

            # search for payment mode related at payment method id
            for pmode in self.env['account.payment.mode'].search(domain):
                mode_ids.append(pmode.id)
            # end for

            # filter domain for payment mode
            return {'domain': {
                'payment_mode_id': [('id', 'in', tuple(mode_ids))]}
            }

    @api.multi
    def generate(self):

        active_ids = self._context.get('active_ids')

        if len(active_ids) > 0:

            lines = self.env['account.move.line'].browse(active_ids)

            # Check for errors standard
            self._raise_on_errors(lines)

            # Check for same bank for invoice_financing
            if self.payment_mode_id.payment_method_code == 'invoice_financing':
                self._check_invoice_financing_line_bank(lines)
                # verifica dati journal bank_account_id
                if self.journal_id and self.journal_id.id:
                    journal = self.journal_id
                    if not journal.bank_account_id.invoice_financing_evaluate:
                        raise UserError('Attenzione!\nMetodo calcolo anticipo non '
                                        'impostato nel conto.')
                    elif journal.bank_account_id.invoice_financing_evaluate \
                            not in ['invoice_amount', 'taxable_amount']:
                        raise UserError('Attenzione!\nMetodo calcolo anticipo '
                                        'ha un valore sconosciuto.')
                    # end if

                    if not journal.bank_account_id.invoice_financing_percent:
                        raise UserError('Attenzione!\nPercentuale di anticipo non '
                                        'impostata nel conto.')
                    # end if

                    if journal.bank_account_id.invoice_financing_percent <= 0:
                        raise UserError('Attenzione!\nLa percentuale di anticipo '
                                        'impostata nel conto deve essere '
                                        'maggiore di zero.')
                    # end if

            # Creazione distinta
            payment_order = self.env['account.payment.order'].create({
                'payment_mode_id': self.payment_mode_id.id,
                'journal_id': self.journal_id.id,
                'description': self.description,
            })

            # Aggiunta linee a distinta
            lines.create_payment_line_from_move_line(payment_order)

            # Apertura ordine di pagamento
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment.order',
                'res_id': payment_order.id,
                'view_mode': 'form',
                'views': [(False, 'form')],
                'target': 'current',
            }
        # end if
    # end generate()

    @api.model
    def _raise_on_errors(self, lines):
        busy_lines = list()
        payment_methods = defaultdict(lambda: {'count': 0, 'name': None})

        for line in lines:

            # Detect lines already assigned to a payment order
            if line.payment_line_ids:
                busy_lines.append(line)
            # end if

            # Check same payment method
            if line.payment_method:
                payment_methods[line.payment_method.id]['count'] += 1
                payment_methods[line.payment_method.id]['name'] = line.payment_method.name
            else:
                payment_methods[-1]['count'] += 1
                payment_methods[-1]['name'] = 'Non impostato'
        # end for

        error_busy = len(busy_lines) > 0
        error_method = len(payment_methods) > 1

        if error_busy or error_method:

            error_msg_busy = ''
            if error_busy:
                error_msg_busy = self._error_msg_busy(busy_lines)
            # end if

            error_msg_method = ''
            if error_method:
                error_msg_method = self._error_msg_method(payment_methods)
            # end if

            # Separate error messages with two newlines if both error
            # messages should be displayed
            error_msg_busy += (error_busy and error_method and '\n\n\n') or ''

            raise UserError(error_msg_busy + error_msg_method)
        # end if
    # end _check_for_errors

    @staticmethod
    def _error_msg_busy(busy_lines):
        msg = 'ATTENZIONE!\nLe seguenti righe ' \
              'sono già parte di una distinta:\n\n - '

        msg += '\n - '.join(
            map(
                lambda x: x.invoice_id.number + '    ' + str(x.date_maturity),
                busy_lines
            )
        )

        return msg
    # end _error_msg_busy

    @staticmethod
    def _error_msg_method(payment_methods):
        msg = 'ATTENZIONE!\nSono state selezionate righe' \
              ' con più metodi di pagamento:\n\n - '

        msg += '\n - '.join(
            map(
                lambda x: x['name'],
                payment_methods.values()
            )
        )

        return msg
    # end _error_msg_method

    @api.model
    def _check_invoice_financing_line_bank(self, lines):
        for line in lines:
            if line.move_id.invoice_bank_id.id:
                invoice_bank_id = line.move_id.invoice_bank_id.id
                if invoice_bank_id != self.journal_id.bank_account_id.id:
                    raise UserError('ATTENZIONE!\nConto bancario aziendale '
                                    'selezionato non corrispondente a quello '
                                    'impostato nelle scadenze.')
        # end for
    # end _check_invoice_financing_line_bank

# end AccountPaymentGenerate
