# Copyright 2021 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import date
# from odoo import fields
from odoo.tools.float_utils import float_round
from odoo.tests.common import TransactionCase
# from dateutil.relativedelta import relativedelta


class TestAssets(TransactionCase):

    def setUp(self):
        super().setUp()
        self.data_account_type_current_assets = self.env.ref(
            'account.data_account_type_current_assets')
        self.data_account_type_current_liabilities = self.env.ref(
            'account.data_account_type_current_liabilities')
        account_model = self.env['account.account']
        self.account_fixed_assets = account_model.search(
            [('user_type_id',
              '=',
              self.env.ref('account.data_account_type_fixed_assets').id)
             ], limit=1)[0]
        self.account_depreciation = account_model.search(
            [('user_type_id',
              '=',
              self.env.ref('account.data_account_type_expenses').id)
             ], limit=1)[0]
        self.account_fund = account_model.search(
            [('user_type_id',
              '=',
              self.env.ref('account.data_account_type_non_current_assets').id)
             ], limit=1)[0]
        self.account_gain = account_model.search(
            [('user_type_id',
              '=',
              self.env.ref('account.data_account_type_revenue').id)
             ], limit=1)[0]
        self.account_loss = account_model.search(
            [('user_type_id',
              '=',
              self.env.ref('account.data_account_type_expenses').id)
             ], limit=1)[0]
        self.journal = self.env['account.journal'].search(
            [('type', '=', 'general')], limit=1)[0]

        self.asset_category_1 = self._create_category(1)
        self.asset_category_2 = self._create_category(2)
        self.asset_1 = self._create_asset(1)
        self.asset_2 = self._create_asset(2)
        for year in range(date.today().year - 2, date.today().year + 1):
            self.env['account.fiscal.year'].create({
                'name': '%s' % year,
                'date_from': date(year, 1, 1),
                'date_to': date(year, 12, 31),
            })

    # TDDO> Remove before publish final code
    def tearDown(self):
        super().tearDown()
        self.env.cr.commit()               # pylint: disable=invalid-commit

    def _create_category(self, cat_nr):
        category = self.env['asset.category'].create({
            'name': 'Asset category #%s' % cat_nr,
            'asset_account_id': self.account_fixed_assets.id,
            'depreciation_account_id': self.account_depreciation.id,
            'fund_account_id': self.account_fund.id,
            'gain_account_id': self.account_gain.id,
            'loss_account_id': self.account_loss.id,
            'journal_id': self.journal.id,
        })
        if cat_nr == 1:
            for rec in self.env['asset.category.depreciation.type'].search(
                [('category_id', '=', category.id)]
            ):
                rec.write(
                    {
                        'percentage': 25,
                        'pro_rata_temporis': False,
                        'mode_id':
                            self.env.ref('assets_management.ad_mode_materiale').id,
                    }
                )
        elif cat_nr == 2:
            for rec in self.env['asset.category.depreciation.type'].search(
                [('category_id', '=', category.id)]
            ):
                rec.write(
                    {
                        'percentage': 24,
                        'pro_rata_temporis': True,
                        'mode_id':
                            self.env.ref('assets_management.ad_mode_immateriale').id,
                    }
                )
        return category

    def _create_asset(self, asset_nr):
        return self.env['asset.asset'].create({
            'name': 'Test asset #%s' % asset_nr,
            'category_id':
                self.asset_category_1.id if asset_nr == 1 else self.asset_category_2.id,
            'company_id': self.env.ref('base.main_company').id,
            'currency_id': self.env.ref('base.main_company').currency_id.id,
            'purchase_amount': 1000.0 if asset_nr == 1 else 2500,
            'purchase_date':
                date(date.today().year - 2, 12, 1)
                if asset_nr == 1 else date(date.today().year - 2, 10, 1),
        })

    def _test_asset_1(self):
        # We test 3 years depreciations:
        # 1. From 01-10-(year-2) to 31-12(year-2) -> 50% rate (asset #1)
        # 2. From 01-01-(year-1) to 31-12(year-1) -> Full year depreciation (100% rate)
        # 3. From 01-01-(year) to today -> unpredictable partial depreciation

        asset = self.asset_1
        self.assertEqual(asset.state,
                         'non_depreciated',
                         'Asset is not in non depreciated state!')

        wiz_vals = asset.with_context(
            {'allow_reload_window': True}
        ).launch_wizard_generate_depreciations()
        wiz = self.env['wizard.asset.generate.depreciation'].with_context(
            wiz_vals['context']
        ).create({})

        deps_amount = {}
        # Year #1: Generate 50% depreciation -> 1000.00€ * 25% * 50% = 125.0€
        year = date.today().year - 2
        wiz.date_dep = date(year, 12, 31)
        wiz.do_generate()
        for dep in asset.depreciation_ids:
            self.assertEqual(float_round(dep.amount_depreciated, 2),
                             125.0,
                             'Invalid depreciation amount!')
            if dep not in deps_amount:
                deps_amount[dep] = dep.amount_depreciated
        # Year #2: Depreciation amount is 250€ (1000€ * 25%)
        year = date.today().year - 1
        wiz.date_dep = date(year, 12, 31)
        wiz.do_generate()
        for dep in asset.depreciation_ids:
            deps_amount[dep] += 250.0
            self.assertEqual(float_round(dep.amount_depreciated, 2),
                             float_round(deps_amount[dep], 2),
                             'Invalid depreciation amount!')
        # Year #3: Current depreciation amount depends on today: value is <= 250€
        wiz.date_dep = date.today()
        wiz.do_generate()
        for dep in asset.depreciation_ids:
            deps_amount[dep] += 250.0
            self.assertLessEqual(float_round(dep.amount_depreciated, 2),
                                 float_round(deps_amount[dep], 2),
                                 'Invalid depreciation amount!')

    def _test_asset_2(self):
        # We test 3 years depreciations:
        # 1. From 01-10-(year-2) to 31-12(year-2) -> 92 days depreciation (asset #2)
        # 2. From 01-01-(year-1) to 31-12(year-1) -> Full year depreciation (100% rate)
        # 3. From 01-01-(year) to today -> unpredictable partial depreciation

        asset = self.asset_2
        self.assertEqual(asset.state,
                         'non_depreciated',
                         'Asset is not in non depreciated state!')

        wiz_vals = asset.with_context(
            {'allow_reload_window': True}
        ).launch_wizard_generate_depreciations()
        wiz = self.env['wizard.asset.generate.depreciation'].with_context(
            wiz_vals['context']
        ).create({})

        deps_amount = {}
        # Year #1: Generate 92 days depreciation -> 2500.00€ * 24% * 92 / 365 = 151.23€
        # If year - 2 is leap depreciation value is 150.82€
        year = date.today().year - 2
        wiz.date_dep = date(year, 12, 31)
        wiz.do_generate()
        for dep in asset.depreciation_ids:
            self.assertGreaterEqual(float_round(dep.amount_depreciated, 2),
                                    150.82,
                                    'Invalid depreciation amount!')
            self.assertLessEqual(float_round(dep.amount_depreciated, 2),
                                 151.23,
                                 'Invalid depreciation amount!')
            if dep not in deps_amount:
                deps_amount[dep] = dep.amount_depreciated
        # Depreciation amount is 600€ (2500€ * 24%)
        year = date.today().year - 1
        wiz.date_dep = date(year, 12, 31)
        wiz.do_generate()
        for dep in asset.depreciation_ids:
            deps_amount[dep] += 600.0
            self.assertEqual(float_round(dep.amount_depreciated, 2),
                             float_round(deps_amount[dep], 2),
                             'Invalid depreciation amount!')
        # Current depreciation amount depends on today: value is <= 600€
        wiz.date_dep = date.today()
        wiz.do_generate()
        for dep in asset.depreciation_ids:
            deps_amount[dep] += 600.0
            self.assertLessEqual(float_round(dep.amount_depreciated, 2),
                                 float_round(deps_amount[dep], 2),
                                 'Invalid depreciation amount!')

    def test_asset(self):
        self._test_asset_1()
        self._test_asset_2()
