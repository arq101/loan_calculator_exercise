#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from decimal import Decimal

from loan_calculator import SimpleLoanCalculator


class TestLoanCalculatorDataValidation(unittest.TestCase):
    
    def setUp(self):
        self.loan_min = 1000
        self.loan_max = 15000

    def test_file_exists(self):
        lc_obj = SimpleLoanCalculator(
            './test_data/test_data_1.csv', self.loan_min)
        self.assertTrue(lc_obj._check_file_exists())

    def test_file_not_found(self):
        lc_obj = SimpleLoanCalculator('./test_data/foo_bar.csv', self.loan_min)
        with self.assertRaises(FileNotFoundError):
            lc_obj._check_file_exists()

    def test_csv_reader_object_has_data(self):
        lc_obj = SimpleLoanCalculator(
            './test_data/test_data_1.csv', self.loan_min)
        reader = lc_obj._read_csv_file()
        data_rows = sum(1 for row in reader)
        self.assertEqual(data_rows, 7)
        lc_obj.file_handle.close()

    def test_csv_reader_object_with_no_data_rows(self):
        lc_obj = SimpleLoanCalculator(
            './test_data/test_data_2.csv', self.loan_min)
        try:
            with self.assertRaises(ValueError):
                lc_obj._read_csv_file()
        finally:
            lc_obj.file_handle.close()

    def test_unexpected_number_of_columns_in_csv_file(self):
        lc_obj = SimpleLoanCalculator(
            './test_data/test_data_3.csv', self.loan_min)
        try:
            with self.assertRaises(ValueError):
                lc_obj._read_csv_file()
        finally:
            lc_obj.file_handle.close()

    def test_is_requested_loan_amount_valid(self):
        lc_obj = SimpleLoanCalculator(
            './test_data/test_data_1.csv', self.loan_min)
        self.assertTrue(lc_obj._is_requested_loan_amount_valid())

    def test_requested_loan_amount_below_minimum_limit(self):
        lc_obj = SimpleLoanCalculator(
            './test_data/test_data_1.csv', self.loan_min-1)
        with self.assertRaises(ValueError):
            lc_obj._is_requested_loan_amount_valid()

    def test_requested_loan_amount_above_max_limit(self):
        lc_obj = SimpleLoanCalculator(
            './test_data/test_data_1.csv', self.loan_max+1)
        with self.assertRaises(ValueError):
            lc_obj._is_requested_loan_amount_valid()

    def test_if_requested_loan_amount_not_in_100_increments(self):
        lc_obj = SimpleLoanCalculator(
            './test_data/test_data_1.csv', self.loan_max+40)
        with self.assertRaises(ValueError):
            lc_obj._is_requested_loan_amount_valid()


class TestLoanCalculator(unittest.TestCase):

    def setUp(self):
        self.loan_min = 1000
        self.loan_max = 15000

    def test_get_lowest_suitable_interest_rate_from_lenders(self):
        lc_obj = SimpleLoanCalculator(
            './test_data/test_data_1.csv', self.loan_min)
        interest_rate = lc_obj.get_lowest_suitable_rate_from_lenders()
        self.assertEqual(interest_rate, '0.069')

    def test_calculate_quote_using_monthly_compounding(self):
        lc_obj = SimpleLoanCalculator(
            './test_data/test_data_1.csv', 5000)
        interest_rate = '0.05'
        principle_amount, interest_rate_percentage, repayments = \
            lc_obj.calculate_quote_using_monthly_compounding(interest_rate)
        self.assertEqual(principle_amount, Decimal('5807.36'))
        self.assertEqual(interest_rate_percentage, Decimal('5.0'))
        self.assertEqual(repayments, Decimal('161.32'))


if __name__ == '__main__':
    unittest.main(verbosity=2)

