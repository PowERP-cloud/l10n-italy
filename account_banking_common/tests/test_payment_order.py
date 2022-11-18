import os
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)

# For some model we use test data in z0bug_odoo and so, we do not declare values dict
# See (https://github.com/zeroincombenze/tools)
TEST_ACCOUNT_JOURNAL = {
    "z0bug.bank11_journal": {},
}
TEST_ACCOUNT_PAYMENT_METHOD = {
    "account_banking_riba.riba": {
        "name": "RiBa CBI",
        "code": "riba_cbi",
        "payment_type": "inbound",
    },
}
TEST_ACCOUNT_PAYMENT_MODE = {
    "z0bug.pmode_riba": {},
}
TEST_ACCOUNT_PAYMENT_TERM = {
    "z0bug.payment_1": {},
    "z0bug.payment_2": {},
}
TEST_ACCOUNT_PAYMENT_TERM_LINE = {
    "z0bug.payment_1_1": {},
    "z0bug.payment_2_1": {},
    "z0bug.payment_2_2": {},
}
TEST_RES_PARTNER_BANK = {
    "z0bug.bank_company_1": {},
}
TEST_SETUP_LIST = [
    "account.payment.method",
    "account.payment.mode",
    "account.payment.term",
    "account.payment.term.line",
    "res.partner.bank",
    "account.journal",
]


class TestPaymentOrder(SingleTransactionCase):

    def setUp(self):
        super().setUp()
        data = {"TEST_SETUP_LIST": TEST_SETUP_LIST}
        for resource in TEST_SETUP_LIST:
            item = "TEST_%s" % resource.upper().replace(".", "_")
            data[item] = globals()[item]
        self.declare_all_data(data, merge="zerobug")
        xref_bank = "external.%s" % self.env["account.account"].search(
            [("user_type_id",
              "=",
              self.env.ref("account.data_account_type_liquidity").id)])[0].code
        for field in ("default_debit_account_id", "default_credit_account_id"):
            self.add_translation(
                "account.journal",
                field,
                ["z0bug.coa_180003", xref_bank])
        self.setup_env()  # Create test environment

    def tearDown(self):
        super().tearDown()
        if os.environ.get("ODOO_COMMIT_TEST", ""):
            # Save test environment, so it is available to use
            self.env.cr.commit()  # pylint: disable=invalid-commit
            _logger.info("✨ Test data committed")

    def test_mytest(self):
        pass
