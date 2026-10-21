import unittest

from invoice import invoice_total


class InvoiceTotalTest(unittest.TestCase):
    def test_no_discount(self):
        self.assertEqual(invoice_total([(50.0, 2)]), 118.0)

    def test_unknown_code_is_ignored(self):
        self.assertEqual(invoice_total([(50.0, 2)], "NOPE"), 118.0)

    def test_discount_code(self):
        # 100.00 subtotal, 10% off -> 90.00, plus 18% tax -> 106.20
        self.assertEqual(invoice_total([(50.0, 2)], "welcome10"), 106.2)


if __name__ == "__main__":
    unittest.main()
