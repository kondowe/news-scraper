import re
import unittest
import datetime
from util import (
    set_month_range,
    replace_date_with_hour,
    check_phrases,
    check_for_dolar_sign,
)


class TestGenerateDateRange(unittest.TestCase):
    def test_today_date_range(self):
        start, end = set_month_range(1)
        today = datetime.date.today()
        expected_start = today.replace(day=1).strftime("%m/%d/%Y")
        expected_end = today.strftime("%m/%d/%Y")
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    def test_one_month_ago_date_range(self):
        start, end = set_month_range(2)
        today = datetime.date.today()
        expected_start = (
            (today - datetime.timedelta(days=30)).replace(day=1).strftime("%m/%d/%Y")
        )
        expected_end = today.strftime("%m/%d/%Y")
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    def test_six_months_ago_date_range(self):
        start, end = set_month_range(7)
        today = datetime.date.today()
        expected_start = (
            (today - datetime.timedelta(days=180)).replace(day=1).strftime("%m/%d/%Y")
        )
        expected_end = today.strftime("%m/%d/%Y")
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    def test_check_phrases(self):
        text_pattern = "apple"
        text = "I have an apple, he has an apple, we all have apples"

        # Test the function with a count of 0
        count = 0
        result = check_phrases(text_pattern, text, count)
        self.assertEqual(result, 3)

        # Test the function with a non-zero count
        count = 2
        result = check_phrases(text_pattern, text, count)
        self.assertEqual(result, 5)

        # Test the function with a different text pattern
        text_pattern = "banana"
        result = check_phrases(text_pattern, text, count)
        self.assertEqual(result, 0)

        # Test the function with an empty text string
        text = ""
        result = check_phrases(text_pattern, text, count)
        self.assertEqual(result, 2)

    def test_check_for_dollar_sign(self):
        text = "The price is $10.50"
        self.assertTrue(check_for_dolar_sign(text))

        text = "The price is 10 dollars"
        self.assertTrue(check_for_dolar_sign(text))

        text = "The price is 10.00 USD"
        self.assertTrue(check_for_dolar_sign(text))

        text = "The price is 10.50 CAD"
        self.assertFalse(check_for_dolar_sign(text))

        text = "The price is 10.50 euro"
        self.assertFalse(check_for_dolar_sign(text))

        text = "The price is ten dollars"
        self.assertFalse(check_for_dolar_sign(text))


if __name__ == "__main__":
    unittest.main()
