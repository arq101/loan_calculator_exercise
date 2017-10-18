#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from loan_calculator import SimpleLoanCalculator


class TestSimpleLoanCalculator(unittest.TestCase):
    
    def setUp(self):
        self.loan_min = 1000
        self.load_max = 15000

    def test_file_exists(self):
        lc_obj = SimpleLoanCalculator('./test_data/test_data_1.csv', self.loan_min)
        self.assertTrue(lc_obj._check_file_exists())

    def test_file_not_found(self):
        lc_obj = SimpleLoanCalculator('./test_data/foo_bar.csv', self.loan_min)
        with self.assertRaises(FileNotFoundError):
            lc_obj._check_file_exists()

    def test_csv_reader_object(self):
        lc_obj = SimpleLoanCalculator('./test_data/test_data_1.csv', self.loan_min)
        reader = lc_obj._read_csv_file()
        data_rows = sum(1 for row in reader)
        self.assertEqual(data_rows, 7)
        lc_obj.file_handle.close()

    def test_csv_reader_object_with_no_data_rows(self):
        lc_obj = SimpleLoanCalculator('./test_data/test_data_2.csv', self.loan_min)
        try:
            with self.assertRaises(ValueError):
                lc_obj._read_csv_file()
        finally:
            lc_obj.file_handle.close()

    def test_unexpected_number_of_columns_in_csv_file(self):
        lc_obj = SimpleLoanCalculator('./test_data/test_data_3.csv', self.loan_min)
        try:
            with self.assertRaises(ValueError):
                lc_obj._read_csv_file()
        finally:
            lc_obj.file_handle.close()

    def test_is_requested_loan_amount_valid(self):
        lc_obj = SimpleLoanCalculator('./test_data/test_data_1.csv', self.loan_min)
        self.assertTrue(lc_obj._is_requested_loan_amount_valid())

    def test_is_requested_loan_amount_valid_if_string(self):
        lc_obj = SimpleLoanCalculator('./test_data/test_data_1.csv', '1000')
        self.assertTrue(lc_obj._is_requested_loan_amount_valid())

    def test_is_requested_loan_amount_valid_if_nonconvertable_string(self):
        lc_obj = SimpleLoanCalculator('./test_data/test_data_1.csv', 'fubar')
        self.assertFalse(lc_obj._is_requested_loan_amount_valid())

    def test_is_requested_loan_amount_below_minimum_limit(self):
        lc_obj = SimpleLoanCalculator('./test_data/test_data_1.csv', self.loan_min-1)
        self.assertFalse(lc_obj._is_requested_loan_amount_valid())

    def test_is_requested_loan_amount_above_max_limit(self):
        lc_obj = SimpleLoanCalculator('./test_data/test_data_1.csv', self.load_max+1)
        self.assertFalse(lc_obj._is_requested_loan_amount_valid())


if __name__ == '__main__':
    unittest.main(verbosity=2)

