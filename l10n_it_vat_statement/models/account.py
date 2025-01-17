# Copyright 2011-12 Domsense s.r.l. <http://www.domsense.com>.
# Copyright 2012-15 Agile Business Group sagl <http://www.agilebg.com>
# Copyright 2015 Associazione Odoo Italia <http://www.odoo-italia.org>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import math
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
from odoo.tools import float_is_zero
import logging

_logger = logging.getLogger(__file__)


class AccountVatPeriodEndStatement(models.Model):
    _name = "account.vat.period.end.statement"
    _description = "VAT period end statement"
    _rec_name = 'date'

    @api.multi
    def _compute_authority_vat_amount(self):
        for statement in self:
            debit_vat_amount = 0.0
            credit_vat_amount = 0.0
            generic_vat_amount = 0.0
            for debit_line in statement.debit_vat_account_line_ids:
                if debit_line.tax_id.tax_group_id.country_id.code != 'IT':
                    to_add = 0.0
                else:
                    to_add = debit_line.deductible_amount

                debit_vat_amount += to_add

            for credit_line in statement.credit_vat_account_line_ids:
                credit_vat_amount += credit_line.amount
            for generic_line in statement.generic_vat_account_line_ids:
                generic_vat_amount += generic_line.amount
            authority_amount = (
                debit_vat_amount
                - credit_vat_amount
                - generic_vat_amount
                - statement.previous_credit_vat_amount
                + statement.previous_debit_vat_amount
                - statement.tax_credit_amount
                + statement.interests_debit_vat_amount
                - statement.advance_amount
            )
            statement.authority_vat_amount = authority_amount

    @api.multi
    def _compute_deductible_vat_amount(self):
        for statement in self:
            credit_vat_amount = 0.0
            for credit_line in statement.credit_vat_account_line_ids:
                credit_vat_amount += credit_line.deductible_amount
            statement.deductible_vat_amount = credit_vat_amount

    @api.multi
    @api.depends(
        'state',
        'move_id.line_ids.amount_residual',
        'move_id.line_ids.currency_id',
    )
    def _compute_residual(self):
        precision = self.env.user.company_id.currency_id.decimal_places
        for statement in self:
            if not statement.move_id.exists():
                statement.residual = 0.0
                statement.reconciled = False
                continue

            residual = 0.0
            for line in statement.move_id.line_ids:
                authority_vat_account_id = (
                    statement.authority_vat_account_id.id
                )
                if line.account_id.id == authority_vat_account_id:
                    residual += line.amount_residual
            statement.residual = abs(residual)
            if float_is_zero(statement.residual, precision_digits=precision):
                statement.reconciled = True
            else:
                statement.reconciled = False

    @api.depends('move_id.line_ids.amount_residual')
    @api.multi
    def _compute_lines(self):
        for statement in self:
            payment_lines = []
            if statement.move_id.exists():
                for line in statement.move_id.line_ids:
                    payment_lines.extend(
                        [
                            _f
                            for _f in [
                                rp.credit_move_id.id
                                for rp in line.matched_credit_ids
                            ]
                            if _f
                        ]
                    )
                    payment_lines.extend(
                        [
                            _f
                            for _f in [
                                rp.debit_move_id.id
                                for rp in line.matched_debit_ids
                            ]
                            if _f
                        ]
                    )
            statement.payment_ids = self.env['account.move.line'].browse(
                list(set(payment_lines))
            )

    @api.model
    def _get_default_interest(self):
        company = self.env.user.company_id
        return company.of_account_end_vat_statement_interest

    @api.model
    def _get_default_interest_percent(self):
        company = self.env.user.company_id
        if not company.of_account_end_vat_statement_interest:
            return 0
        return company.of_account_end_vat_statement_interest_percent

    debit_vat_account_line_ids = fields.One2many(
        'statement.debit.account.line',
        'statement_id',
        'Debit line VAT',
        help='The accounts containing the debit VAT amount to write-off',
        readonly=True,
    )
    credit_vat_account_line_ids = fields.One2many(
        'statement.credit.account.line',
        'statement_id',
        'Credit line VAT',
        help='The accounts containing the credit VAT amount to write-off',
        readonly=True,
    )
    previous_credit_vat_account_id = fields.Many2one(
        'account.account',
        'Previous Credits VAT',
        help='Credit VAT from previous periods',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
    )
    previous_credit_vat_amount = fields.Float(
        'Previous Credits VAT Amount',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
        digits=dp.get_precision('Account'),
    )
    previous_year_credit = fields.Boolean("Previous year credits")
    previous_debit_vat_account_id = fields.Many2one(
        'account.account',
        'Previous Debits VAT',
        help='Debit VAT from previous periods',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
    )
    previous_debit_vat_amount = fields.Float(
        'Previous Debits VAT Amount',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
        digits=dp.get_precision('Account'),
    )
    interests_debit_vat_account_id = fields.Many2one(
        'account.account',
        'Due interests',
        help='Due interests for three-monthly statments',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
    )
    interests_debit_vat_amount = fields.Float(
        'Due interests Amount',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
        digits=dp.get_precision('Account'),
    )
    tax_credit_account_id = fields.Many2one(
        'account.account',
        'Tax credits',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
    )
    tax_credit_amount = fields.Float(
        'Tax credits Amount',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
        digits=dp.get_precision('Account'),
    )
    advance_account_id = fields.Many2one(
        'account.account',
        'Down payment',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
    )
    advance_amount = fields.Float(
        'Down payment Amount',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
        digits=dp.get_precision('Account'),
    )
    generic_vat_account_line_ids = fields.One2many(
        'statement.generic.account.line',
        'statement_id',
        'Other VAT Credits / Debits or Tax Compensations',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
    )
    authority_partner_id = fields.Many2one(
        'res.partner',
        'Tax Authority Partner',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
    )
    authority_vat_account_id = fields.Many2one(
        'account.account',
        'Tax Authority VAT Account',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
    )
    authority_vat_amount = fields.Float(
        'Authority VAT Amount',
        compute="_compute_authority_vat_amount",
        digits=dp.get_precision('Account'),
    )
    # TODO is this field needed?
    deductible_vat_amount = fields.Float(
        'Deductible VAT Amount',
        compute="_compute_deductible_vat_amount",
        digits=dp.get_precision('Account'),
    )
    journal_id = fields.Many2one(
        'account.journal',
        'Journal',
        # required=True,
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
    )
    date = fields.Date(
        'Date',
        required=True,
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
        default=fields.Date.context_today,
    )
    move_id = fields.Many2one(
        'account.move', 'VAT statement move', readonly=True
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('paid', 'Paid'),
        ],
        'State',
        readonly=True,
        default='draft',
    )
    payment_term_id = fields.Many2one(
        'account.payment.term',
        'Payment Term',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)],
        },
    )
    reconciled = fields.Boolean(
        'Paid/Reconciled',
        compute="_compute_residual",
        help="It indicates that the statement has been paid and the "
        "journal entry of the statement has been reconciled with "
        "one or several journal entries of payment.",
        store=True,
        readonly=True,
    )
    residual = fields.Float(
        string='Amount Due',
        compute='_compute_residual',
        store=True,
        help="Remaining amount due.",
        digits=dp.get_precision('Account'),
    )
    payment_ids = fields.Many2many(
        'account.move.line',
        string='Payments',
        compute="_compute_lines",
        store=True,
    )
    # date_range_ids = fields.One2many(
    #     'date.range', 'vat_statement_id', 'Periods')

    date_range_ids = fields.Many2many(
        comodel_name='date.range',
        # 'vat_statement_id',
        string='Periods',
    )
    interest = fields.Boolean(
        'Compute Interest', default=_get_default_interest
    )
    interest_percent = fields.Float(
        'Interest - Percent', default=_get_default_interest_percent
    )
    fiscal_page_base = fields.Integer(
        'Last printed page', required=True, default=0
    )
    fiscal_year = fields.Char('Fiscal year for report')
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'account.invoice'
        ),
    )
    annual = fields.Boolean("Annual prospect")

    debit_vat_group_line_ids = fields.One2many(
        comodel_name='statement.debit.group.line',
        inverse_name='statement_id',
        string='Debit group line VAT',
        help='The accounts containing the VAT amount total to write-off',
        readonly=True,
    )

    credit_vat_group_line_ids = fields.One2many(
        comodel_name='statement.credit.group.line',
        inverse_name='statement_id',
        string='Credit group line VAT',
        help='The accounts containing the VAT amount total to write-off',
        readonly=True,
    )

    name = fields.Text(string='Descrizione')

    statement_type = fields.Selection(
        [
            ('recur', 'Liquidazione periodica'),
            ('year', 'Liquidazione annuale'),
            ('eu', 'Liquidazione EU-OSS'),
        ],
        string='Tipo liquidazione',
        required=True,
        default='recur',
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
        default=lambda self: self.env.user.company_id.country_id,
    )

    @api.multi
    def unlink(self):
        for statement in self:
            if statement.state == 'confirmed' or statement.state == 'paid':
                raise UserError(
                    _('You cannot delete a confirmed or paid statement')
                )
        res = super(AccountVatPeriodEndStatement, self).unlink()
        return res

    @api.multi
    def set_fiscal_year(self):
        for statement in self:
            if statement.date_range_ids:
                date = min([x.date_start for x in statement.date_range_ids])
                statement.update({'fiscal_year': date.year})

    @api.multi
    def _write(self, vals):
        pre_not_reconciled = self.filtered(
            lambda statement: not statement.reconciled
        )
        pre_reconciled = self - pre_not_reconciled
        res = super(AccountVatPeriodEndStatement, self)._write(vals)
        reconciled = self.filtered(lambda statement: statement.reconciled)
        not_reconciled = self - reconciled
        (reconciled & pre_reconciled).filtered(
            lambda statement: statement.state == 'confirmed'
        ).statement_paid()
        (not_reconciled & pre_not_reconciled).filtered(
            lambda statement: statement.state == 'paid'
        ).statement_confirmed()
        return res

    @api.multi
    def statement_draft(self):
        for statement in self:
            if statement.move_id:
                statement.move_id.button_cancel()
                statement.move_id.unlink()
            statement.state = 'draft'

    @api.multi
    def statement_paid(self):
        for statement in self:
            statement.state = 'paid'

    @api.multi
    def statement_confirmed(self):
        for statement in self:
            statement.state = 'confirmed'

    @api.multi
    def create_move(self):
        move_obj = self.env['account.move']
        for statement in self:
            statement_date = fields.Date.to_string(statement.date)
            move_data = {
                'name': _('VAT statement') + ' - ' + statement_date,
                'date': statement_date,
                'journal_id': statement.journal_id.id,
            }
            move = move_obj.create(move_data)
            move_id = move.id
            statement.write({'move_id': move_id})
            lines_to_create = []

            for debit_line in statement.debit_vat_account_line_ids:
                if debit_line.tax_id.tax_group_id.country_id.code != 'IT':
                    continue
                if debit_line.amount != 0.0 and debit_line.account_id:
                    debit_vat_data = {
                        'name': _('Debit VAT'),
                        'account_id': debit_line.account_id.id,
                        'move_id': move_id,
                        'journal_id': statement.journal_id.id,
                        'debit': 0.0,
                        'credit': 0.0,
                        'date': statement_date,
                        'company_id': statement.company_id.id,
                    }

                    if debit_line.amount > 0:
                        debit_vat_data['debit'] = math.fabs(debit_line.amount)
                    else:
                        debit_vat_data['credit'] = math.fabs(debit_line.amount)
                    lines_to_create.append((0, 0, debit_vat_data))

            for credit_line in statement.credit_vat_account_line_ids:
                if credit_line.amount != 0.0 and credit_line.account_id:
                    credit_vat_data = {
                        'name': _('Credit VAT'),
                        'account_id': credit_line.account_id.id,
                        'move_id': move_id,
                        'journal_id': statement.journal_id.id,
                        'debit': 0.0,
                        'credit': 0.0,
                        'date': statement_date,
                        'company_id': statement.company_id.id,
                    }
                    if credit_line.amount < 0:
                        credit_vat_data['debit'] = math.fabs(
                            credit_line.amount
                        )
                    else:
                        credit_vat_data['credit'] = math.fabs(
                            credit_line.amount
                        )
                    lines_to_create.append((0, 0, credit_vat_data))

            if statement.previous_credit_vat_amount:
                previous_credit_vat_data = {
                    'name': _('Previous Credits VAT'),
                    'account_id': statement.previous_credit_vat_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement_date,
                    'company_id': statement.company_id.id,
                }
                if statement.previous_credit_vat_amount < 0:
                    previous_credit_vat_data['debit'] = math.fabs(
                        statement.previous_credit_vat_amount
                    )
                else:
                    previous_credit_vat_data['credit'] = math.fabs(
                        statement.previous_credit_vat_amount
                    )
                lines_to_create.append((0, 0, previous_credit_vat_data))

            if statement.tax_credit_amount:
                tax_credit_vat_data = {
                    'name': _('Tax Credits'),
                    'account_id': statement.tax_credit_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement_date,
                    'company_id': statement.company_id.id,
                }
                if statement.tax_credit_amount < 0:
                    tax_credit_vat_data['debit'] = math.fabs(
                        statement.tax_credit_amount
                    )
                else:
                    tax_credit_vat_data['credit'] = math.fabs(
                        statement.tax_credit_amount
                    )
                lines_to_create.append((0, 0, tax_credit_vat_data))

            if statement.advance_amount:
                advance_vat_data = {
                    'name': _('Tax Credits'),
                    'account_id': statement.advance_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement_date,
                    'company_id': statement.company_id.id,
                }
                if statement.advance_amount < 0:
                    advance_vat_data['debit'] = math.fabs(
                        statement.advance_amount
                    )
                else:
                    advance_vat_data['credit'] = math.fabs(
                        statement.advance_amount
                    )
                lines_to_create.append((0, 0, advance_vat_data))

            if statement.previous_debit_vat_amount:
                previous_debit_vat_data = {
                    'name': _('Previous Debits VAT'),
                    'account_id': statement.previous_debit_vat_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement_date,
                    'company_id': statement.company_id.id,
                }
                if statement.previous_debit_vat_amount > 0:
                    previous_debit_vat_data['debit'] = math.fabs(
                        statement.previous_debit_vat_amount
                    )
                else:
                    previous_debit_vat_data['credit'] = math.fabs(
                        statement.previous_debit_vat_amount
                    )
                lines_to_create.append((0, 0, previous_debit_vat_data))

            if statement.interests_debit_vat_amount:
                interests_data = {
                    'name': _('Due interests'),
                    'account_id': statement.interests_debit_vat_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement_date,
                    'company_id': statement.company_id.id,
                }
                if statement.interests_debit_vat_amount > 0:
                    interests_data['debit'] = math.fabs(
                        statement.interests_debit_vat_amount
                    )
                else:
                    interests_data['credit'] = math.fabs(
                        statement.interests_debit_vat_amount
                    )
                lines_to_create.append((0, 0, interests_data))

            for generic_line in statement.generic_vat_account_line_ids:
                generic_vat_data = {
                    'name': _('Other VAT Credits / Debits'),
                    'account_id': generic_line.account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement_date,
                    'company_id': statement.company_id.id,
                }
                if generic_line.amount < 0:
                    generic_vat_data['debit'] = math.fabs(generic_line.amount)
                else:
                    generic_vat_data['credit'] = math.fabs(generic_line.amount)
                lines_to_create.append((0, 0, generic_vat_data))

            end_debit_vat_data = {
                'name': _('Tax Authority VAT'),
                'account_id': statement.authority_vat_account_id.id,
                'partner_id': statement.authority_partner_id.id,
                'move_id': move_id,
                'journal_id': statement.journal_id.id,
                'date': statement_date,
                'company_id': statement.company_id.id,
            }
            if statement.authority_vat_amount > 0:
                end_debit_vat_data['debit'] = 0.0
                end_debit_vat_data['credit'] = math.fabs(
                    statement.authority_vat_amount
                )
                if statement.payment_term_id:
                    due_list = statement.payment_term_id.compute(
                        statement.authority_vat_amount, statement_date
                    )[0]
                    for term in due_list:
                        current_line = end_debit_vat_data
                        current_line['credit'] = term[1]
                        current_line['date_maturity'] = term[0]
                        lines_to_create.append((0, 0, current_line))
                else:
                    lines_to_create.append((0, 0, end_debit_vat_data))
            elif statement.authority_vat_amount < 0:
                end_debit_vat_data['debit'] = math.fabs(
                    statement.authority_vat_amount
                )
                end_debit_vat_data['credit'] = 0.0
                lines_to_create.append((0, 0, end_debit_vat_data))

            move.line_ids = lines_to_create
            move.post()
            statement.state = 'confirmed'

        return True

    @api.multi
    def compute_amounts(self):
        decimal_precision_obj = self.env['decimal.precision']
        debit_line_model = self.env['statement.debit.account.line']
        credit_line_model = self.env['statement.credit.account.line']

        for statement in self:

            statement.previous_debit_vat_amount = 0.0
            prev_statements = self.search(
                [
                    ('date', '<', statement.date),
                    ('statement_type', 'not in', ('year', 'eu')),
                ],
                order='date desc',
            )
            if prev_statements and statement.statement_type not in [
                'year',
                'eu',
            ]:
                # not statement.annual:

                prev_statement = prev_statements[0]
                if (
                    prev_statement.residual > 0
                    and prev_statement.authority_vat_amount > 0
                ):
                    statement.write(
                        {'previous_debit_vat_amount': prev_statement.residual}
                    )
                elif prev_statement.authority_vat_amount < 0:
                    statement.write(
                        {
                            'previous_credit_vat_amount': (
                                -prev_statement.authority_vat_amount
                            )
                        }
                    )
                    company = statement.company_id or self.env.user.company_id
                    statement_fiscal_year_dates = (
                        company.compute_fiscalyear_dates(
                            statement.date_range_ids
                            and statement.date_range_ids[0].date_start
                            or statement.date
                        )
                    )
                    prev_statement_fiscal_year_dates = (
                        company.compute_fiscalyear_dates(
                            prev_statement.date_range_ids
                            and prev_statement.date_range_ids[0].date_start
                            or prev_statement.date
                        )
                    )
                    if (
                        prev_statement_fiscal_year_dates['date_to']
                        < statement_fiscal_year_dates['date_from']
                    ):
                        statement.write({'previous_year_credit': True})

            credit_line_ids, debit_line_ids = self._get_credit_debit_lines(
                statement
            )

            for debit_line in statement.debit_vat_account_line_ids:
                debit_line.unlink()
            for credit_line in statement.credit_vat_account_line_ids:
                credit_line.unlink()
            for debit_vals in debit_line_ids:
                debit_vals.update({'statement_id': statement.id})
                debit_line_model.create(debit_vals)
            for credit_vals in credit_line_ids:
                credit_vals.update({'statement_id': statement.id})
                credit_line_model.create(credit_vals)

            interest_amount = 0.0
            # if exits Delete line with interest
            acc_id = self.get_account_interest().id
            statement.interests_debit_vat_account_id = None
            statement.interests_debit_vat_amount = interest_amount

            # Compute interest
            if statement.interest and statement.authority_vat_amount > 0:
                interest_amount = round(
                    statement.authority_vat_amount
                    * (float(statement.interest_percent) / 100),
                    decimal_precision_obj.precision_get('Account'),
                )
            # Add line with interest
            if interest_amount:
                statement.interests_debit_vat_account_id = acc_id
                statement.interests_debit_vat_amount = interest_amount

            # clean up
            statement._clean_group_total()

            # Add group lines
            statement._set_group_lines('credit')
            statement._set_group_lines('debit')

        return True

    def _clean_group_total(self):

        for model in (
            self.env['statement.debit.group.line'],
            self.env['statement.credit.group.line'],
        ):
            lines = model.search([('statement_id', '=', self.id)])
            if lines:
                for line in lines:
                    line.unlink()

    def evaluate_tax_values(self, tax, statement):
        reg_type = {'sale': 'customer', 'purchase': 'supplier'}.get(
            tax.type_tax_use, ''
        )
        total_base = total_vat = total = 0.0
        for period in statement.date_range_ids:
            total_base, total_vat, total = map(
                sum,
                zip((total_base, total_vat, total)),
                tax.compute_totals_tax(
                    {
                        'from_date': period.date_start,
                        'to_date': period.date_end,
                        'registry_type': reg_type,
                    }
                )[1:4],
            )
        # set account id from tax children
        account_id = False
        if not tax.account_id.id and tax.children_tax_ids:
            for child in tax.children_tax_ids:
                if child.account_id.id:
                    account_id = child.account_id.id
        else:
            account_id = tax.account_id.id

        return {
            'kind_id': tax.kind_id.id if tax.kind_id else False,
            # 'account_id': tax.account_id.id if tax.account_id else False,
            'account_id': account_id,
            'tax_id': tax.id,
            'base_amount': total_base,
            'vat_amount': total_vat,
            'amount': total,
        }, bool(total or total_base or total_vat)

    def sum_to_account(self, vals, total):
        def sum_item(id, level, vals, total):
            hash = '%s-%s' % (level, id)
            if hash not in total:
                total[hash] = {
                    'level': level,
                }
                if level == 'N':
                    for nm in ('kind_id', 'nature_code'):
                        total[hash][nm] = vals.get(nm, False)
                else:
                    total[hash]['account_id'] = vals.get('account_id', False)
                    total[hash]['tax_id'] = vals['tax_id']
                for nm in ('amount', 'base_amount', 'vat_amount'):
                    total[hash][nm] = 0.0
            for nm in ('amount', 'base_amount', 'vat_amount'):
                total[hash][nm] += vals[nm]
            if level == 'A' and vals['tax_id'] != total[hash]['tax_id']:
                total[hash]['tax_id'] = False
            return total

        return sum_item(
            vals['nature_code'],
            'N',
            vals,
            sum_item(vals.get('account_id') or '~', 'A', vals, total),
        )

    def _set_dbtcrd_lines(self, tax, line_ids, statement, total):
        vals, valid = self.evaluate_tax_values(tax, statement)
        if valid:
            line_ids.append(vals)
            vals['nature_code'] = tax.kind_id.code if tax.kind_id else ' '
            total = self.sum_to_account(vals, total)
        return line_ids, total

    def split_line_total(self, total):
        kind_ids = []
        line_ids = []
        for hash in sorted(total.keys()):
            vals = total[hash]
            level = vals['level']
            del vals['level']
            if level == 'N':
                kind_ids.append(vals)
            else:
                line_ids.append(vals)
        return kind_ids, line_ids

    def _get_credit_debit_lines(self, statement):
        credit_line_ids = []
        debit_line_ids = []
        credit_total = {}
        debit_total = {}
        tax_model = self.env['account.tax']
        domain = [
            # ('vat_statement_account_id', '!=', False),
            ('type_tax_use', 'in', ['sale', 'purchase']),
            ('company_id', '=', self.company_id.id),
        ]
        # check statement for type
        if statement.statement_type == 'eu':
            # country
            if not statement.country_id:
                raise UserError(
                    'Nazione non impostata per Liquidazione iva EU-OSS'
                )
            # end if

            # group tax with country
            group_ids = self.env['account.tax.group'].search(
                [('country_id', '=', statement.country_id.id)]
            )

            if not group_ids:
                msg = 'Gruppo imposte non trovato per {nazione}'.format(
                    nazione=statement.country_id.name
                )
                raise UserError(msg)

            domain.append(('tax_group_id', 'in', [t.id for t in group_ids]))
        # end if

        taxes = tax_model.search(domain)
        for tax in taxes:
            if any(
                tax_child
                for tax_child in tax.children_tax_ids
                if tax_child.cee_type in ('sale', 'purchase')
            ):

                for tax_child in tax.children_tax_ids:
                    if tax_child.cee_type == 'sale':
                        debit_tax_ids, debit_total = self._set_dbtcrd_lines(
                            tax_child, debit_line_ids, statement, debit_total
                        )
                    elif tax_child.cee_type == 'purchase':
                        credit_tax_ids, credit_total = self._set_dbtcrd_lines(
                            tax_child, credit_line_ids, statement, credit_total
                        )

            elif tax.type_tax_use == 'sale':
                debit_line_ids, debit_total = self._set_dbtcrd_lines(
                    tax, debit_line_ids, statement, debit_total
                )
            elif tax.type_tax_use == 'purchase':
                credit_line_ids, credit_total = self._set_dbtcrd_lines(
                    tax, credit_line_ids, statement, credit_total
                )

        return credit_line_ids, debit_line_ids

    def _set_group_lines(self, type):
        accounts = {}
        kinds = {}
        others = {}
        if type and type in ('credit', 'debit'):
            lines = (
                self.debit_vat_account_line_ids
                if type == 'debit'
                else self.credit_vat_account_line_ids
            )
            # sum amount
            for line in lines:
                if line.account_id:
                    account = line.account_id
                    if account in accounts:
                        accounts[account]['amount'] += line.amount
                        accounts[account]['base_amount'] += line.base_amount
                        accounts[account]['vat_amount'] += line.vat_amount
                        accounts[account][
                            'undeductible_amount'
                        ] += line.undeductible_amount
                        accounts[account][
                            'deductible_amount'
                        ] += line.deductible_amount
                    else:
                        accounts[account] = {
                            'amount': line.amount,
                            'type': 'account',
                            'base_amount': line.base_amount,
                            'vat_amount': line.vat_amount,
                            'undeductible_amount': line.undeductible_amount,
                            'deductible_amount': line.deductible_amount,
                        }
                elif line.tax_id.kind_id:
                    kind_id = line.tax_id.kind_id
                    if kind_id in kinds:
                        kinds[kind_id]['amount'] += line.amount
                        kinds[kind_id]['base_amount'] += line.base_amount
                        kinds[kind_id]['vat_amount'] += line.vat_amount
                        kinds[kind_id][
                            'undeductible_amount'
                        ] += line.undeductible_amount
                        kinds[kind_id][
                            'deductible_amount'
                        ] += line.deductible_amount
                    else:
                        kinds[kind_id] = {
                            'amount': line.amount,
                            'type': 'nature',
                            'base_amount': line.base_amount,
                            'vat_amount': line.vat_amount,
                            'undeductible_amount': line.undeductible_amount,
                            'deductible_amount': line.deductible_amount,
                        }
                else:
                    if 'unique' in others:
                        others['unique']['amount'] += line.amount
                        others['unique']['base_amount'] += line.base_amount
                        others['unique']['vat_amount'] += line.vat_amount
                        others['unique'][
                            'undeductible_amount'
                        ] += line.undeductible_amount
                        others['unique'][
                            'deductible_amount'
                        ] += line.deductible_amount
                    else:
                        others.update(
                            {
                                'unique': {
                                    'amount': line.amount,
                                    'type': 'other',
                                    'base_amount': line.base_amount,
                                    'vat_amount': line.vat_amount,
                                    'undeductible_amount': line.undeductible_amount,
                                    'deductible_amount': line.deductible_amount,
                                }
                            }
                        )

            # end for
            _logger.info(accounts)
            _logger.info(kinds)
            _logger.info(others)

            if accounts:
                self._set_group_totals(accounts, type)
            # end if

            if kinds:
                self._set_group_totals(kinds, type)
            # end if

            if others:
                self._set_group_totals(others, type)
            # end if

    def _set_group_totals(self, totals, type):
        model = (
            self.env['statement.debit.group.line']
            if type == 'debit'
            else self.env['statement.credit.group.line']
        )

        for total, value in totals.items():
            vals = {
                'statement_id': self.id,
                'amount': value['amount'],
                'base_amount': value['base_amount'],
                'vat_amount': value['vat_amount'],
                'undeductible_amount': value['undeductible_amount'],
                'deductible_amount': value['deductible_amount'],
                'account_id': None,
                'name': '',
                'kind_id': None,
            }
            if value['type'] and value['type'] == 'account':
                vals.update(
                    {'account_id': total.id, 'name': total.display_name}
                )
            # end if

            if value['type'] and value['type'] == 'nature':
                vals.update({'kind_id': total.id, 'name': total.display_name})
            # end if

            model.create(vals)

    @api.onchange('authority_partner_id')
    def on_change_partner_id(self):
        self.authority_vat_account_id = (
            self.authority_partner_id.property_account_payable_id.id
        )

    @api.onchange('interest')
    def onchange_interest(self):
        company = self.env.user.company_id
        self.interest_percent = (
            company.of_account_end_vat_statement_interest_percent
        )

    @api.multi
    def get_account_interest(self):
        company = self.env.user.company_id
        if company.of_account_end_vat_statement_interest or any(
            [s.interest for s in self]
        ):
            if not company.of_account_end_vat_statement_interest_account_id:
                raise UserError(
                    _("The account for vat interest must be configurated")
                )

        return company.of_account_end_vat_statement_interest_account_id


class StatementDebitAccountLine(models.Model):
    _name = 'statement.debit.account.line'
    _description = "VAT Statement debit account line"

    @api.depends('tax_id')
    def _compute_deductible_amount(self):
        for line in self:
            if line.tax_id.tax_group_id.country_id.code != 'IT':
                line.deductible_amount = 0.0
            else:
                is_split_payment = getattr(
                    line.tax_id, 'is_split_payment', None
                )
                _logger.info(
                    'is_split_payment {sp}'.format(sp=is_split_payment)
                )
                if (
                    not line.tax_id.account_id
                    or is_split_payment
                    or (
                        line.kind_id.code
                        and line.kind_id.code.startswith('N6')
                    )
                ):
                    line.deductible_amount = 0.0
                else:
                    line.deductible_amount = line.amount
                # end if
            # end if
        # end for

    # end _compute_deductible_amount

    @api.depends('tax_id')
    def _compute_undeductible_amount(self):
        for line in self:
            is_split_payment = getattr(line.tax_id, 'is_split_payment', None)
            if is_split_payment:
                line.undeductible_amount = line.vat_amount
            elif not line.tax_id.account_id or (
                line.kind_id.code and line.kind_id.code.startswith('N6')
            ):
                line.undeductible_amount = line.amount
            else:
                line.undeductible_amount = 0.0
            # end if

        # end for

    # end _compute_undeductible_amount

    account_id = fields.Many2one('account.account', 'Account')
    tax_id = fields.Many2one('account.tax', 'Tax', required=True)
    statement_id = fields.Many2one(
        'account.vat.period.end.statement', 'VAT statement'
    )
    amount = fields.Float(
        'Amount', required=True, digits=dp.get_precision('Account')
    )
    base_amount = fields.Float(
        'Base Amount', digits=dp.get_precision('Account')
    )
    vat_amount = fields.Float('Vat Amount', digits=dp.get_precision('Account'))
    kind_id = fields.Many2one('account.tax.kind', 'Tax nature')

    deductible_amount = fields.Float(
        'Amount',
        compute='_compute_deductible_amount',
        store=True,
    )

    undeductible_amount = fields.Float(
        'Undeductible',
        compute='_compute_undeductible_amount',
        store=True,
    )


class StatementCreditAccountLine(models.Model):
    _name = 'statement.credit.account.line'
    _description = "VAT Statement credit account line"

    @api.depends('tax_id')
    def _compute_deductible_amount(self):
        for line in self:
            line.deductible_amount = line.amount
        # end for

    # end _compute_deductible_amount

    @api.depends('tax_id')
    def _compute_undeductible_amount(self):
        for line in self:
            line.undeductible_amount = line.vat_amount - line.amount
        # end for

    # end _compute_undeductible_amount

    account_id = fields.Many2one('account.account', 'Account')
    tax_id = fields.Many2one('account.tax', 'Tax', required=True)
    statement_id = fields.Many2one(
        'account.vat.period.end.statement', 'VAT statement'
    )
    amount = fields.Float(
        'Amount', required=True, digits=dp.get_precision('Account')
    )
    base_amount = fields.Float(
        'Base Amount', digits=dp.get_precision('Account')
    )
    vat_amount = fields.Float('Vat Amount', digits=dp.get_precision('Account'))
    kind_id = fields.Many2one('account.tax.kind', 'Tax nature')

    deductible_amount = fields.Float(
        'Iva ',
        compute='_compute_deductible_amount',
        store=True,
    )

    undeductible_amount = fields.Float(
        'Undeductible',
        compute='_compute_undeductible_amount',
        store=True,
    )


class StatementGenericAccountLine(models.Model):
    _name = 'statement.generic.account.line'
    _description = "VAT Statement generic account line"
    _sort = 'kind_id, account_id, tax_id'

    account_id = fields.Many2one('account.account', 'Account', required=True)
    statement_id = fields.Many2one(
        'account.vat.period.end.statement', 'VAT statement'
    )
    amount = fields.Float(
        'Amount', required=True, digits=dp.get_precision('Account')
    )
    base_amount = fields.Float(
        'Base Amount', digits=dp.get_precision('Account')
    )
    vat_amount = fields.Float('Vat Amount', digits=dp.get_precision('Account'))
    kind_id = fields.Many2one('account.tax.kind', 'Tax nature')
    name = fields.Char('Description')


# class DateRange(models.Model):
#     _inherit = "date.range"
#     vat_statement_id = fields.Many2one(
#         'account.vat.period.end.statement', "VAT statement"
#     )


class StatementDebitGroupLine(models.Model):
    _name = 'statement.debit.group.line'
    _description = "VAT Statement debit group line"

    statement_id = fields.Many2one(
        'account.vat.period.end.statement', 'VAT statement'
    )

    account_id = fields.Many2one('account.account', 'Account')

    amount = fields.Float(
        'Amount', required=True, digits=dp.get_precision('Account')
    )

    base_amount = fields.Float(
        'Base Amount', digits=dp.get_precision('Account')
    )

    vat_amount = fields.Float('Vat Amount', digits=dp.get_precision('Account'))

    kind_id = fields.Many2one('account.tax.kind', 'Tax nature')

    name = fields.Char(
        string='Description',
        default='',
    )
    deductible_amount = fields.Float(
        'Amount', digits=dp.get_precision('Account')
    )

    undeductible_amount = fields.Float(
        'Undeductible', digits=dp.get_precision('Account')
    )


class StatementCreditGroupLine(models.Model):
    _name = 'statement.credit.group.line'
    _description = "VAT Statement credit group line"

    statement_id = fields.Many2one(
        'account.vat.period.end.statement', 'VAT statement'
    )

    account_id = fields.Many2one('account.account', 'Account')

    amount = fields.Float(
        'Importo', required=True, digits=dp.get_precision('Account')
    )

    base_amount = fields.Float(
        'Base Amount', digits=dp.get_precision('Account')
    )

    vat_amount = fields.Float('Vat Amount', digits=dp.get_precision('Account'))

    kind_id = fields.Many2one('account.tax.kind', 'Tax nature')

    name = fields.Char(
        string='Description',
        default='',
    )

    deductible_amount = fields.Float(
        'Deductible', digits=dp.get_precision('Account')
    )

    undeductible_amount = fields.Float(
        'Undeductible', digits=dp.get_precision('Account')
    )
