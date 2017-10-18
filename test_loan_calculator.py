#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from loan_calculator import SimpleLoanCalculator


class TestSimpleLoanCalculator(unittest.TestCase):

    def test_file_exists(self):
        loan_calc_obj = SimpleLoanCalculator('./test_data/test_data_1.csv', 200)
        self.assertTrue(loan_calc_obj._check_file_exists())

    def test_file_not_found(self):
        loan_calc_obj = SimpleLoanCalculator('./test_data/foo_bar.csv', 200)
        with self.assertRaises(FileNotFoundError):
            loan_calc_obj._check_file_exists()

    def test_csv_reader_object(self):
        loan_calc_obj = SimpleLoanCalculator('./test_data/test_data_1.csv', 200)
        reader = loan_calc_obj._read_csv_file()
        data_rows = sum(1 for row in reader)
        self.assertEqual(data_rows, 7)
        loan_calc_obj.file_handle.close()

    def test_csv_reader_object_with_no_data_rows(self):
        loan_calc_obj = SimpleLoanCalculator('./test_data/test_data_2.csv', 200)
        try:
            with self.assertRaises(ValueError):
                loan_calc_obj._read_csv_file()
        finally:
            loan_calc_obj.file_handle.close()

    def test_unexpected_number_of_columns_in_csv_file(self):
        loan_calc_obj = SimpleLoanCalculator('./test_data/test_data_3.csv', 200)
        try:
            with self.assertRaises(ValueError):
                loan_calc_obj._read_csv_file()
        finally:
            loan_calc_obj.file_handle.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)

