# -*- coding: utf-8 -*-

import os
import csv


class SimpleLoanCalculator(object):
    MIN_LOAN = 1000
    MAX_LOAN = 15000

    def __init__(self, data_file, requested_loan):
        self.market_data_file = data_file
        self.file_handle = None
        self.requested_loan_amount = requested_loan

    def _is_requested_loan_amount_valid(self):
        """ Checks requested loan amount meets upper and lower limits of
        the loan system and is in increments of £100.
        """
        try:
            self.requested_loan_amount = int(self.requested_loan_amount)
        except ValueError:
            return False

        if SimpleLoanCalculator.MIN_LOAN <= self.requested_loan_amount \
                <= SimpleLoanCalculator.MAX_LOAN \
                and self.requested_loan_amount % 100 == 0:
            return True
        else:
            return False

    def _check_file_exists(self):
        if os.path.isfile(os.path.abspath(self.market_data_file)):
            return True
        else:
            print('>> Error: file "{}" not found!'.format(self.market_data_file))
            # then bail out
            raise FileNotFoundError

    def _read_csv_file(self):
        """ Reads and returns a reader object which will iterate over lines in
        the given csv file and maps the column names.

        This method also checks if the csv file has any rows of data and
        that the number of columns are as expected.

        Manually close the file handle
        """
        self._check_file_exists()
        self.file_handle = open(self.market_data_file)
        reader = csv.DictReader(self.file_handle)
        self._verify_number_of_columns_in_csv_file(reader)
        try:
            reader.__next__()

            # csv reader obj will not refresh even if the file handle is
            # "seeked" to 0, so recreate reader obj
            self.file_handle.seek(0)
            reader = csv.DictReader(self.file_handle)
        except StopIteration:
            print('>> Error: file "{}" does not contain data!'.format(
                self.market_data_file))
            raise ValueError
        else:
            return reader

    def _verify_number_of_columns_in_csv_file(self, csv_reader_obj):
        expected_columns = 3
        if len(csv_reader_obj.fieldnames) == expected_columns:
            return
        else:
            print('>> Error: expected {} columns, but found {}!'.format(
                expected_columns, len(csv_reader_obj.fieldnames)))
            raise ValueError

    def _find_lowest_rate_lender(self):
        reader = self._read_csv_file()
        sorted_list = sorted(
            reader, key=lambda row: int(row['Rate']), reverse=True)

