# -*- coding: utf-8 -*-

import os
import csv
from decimal import Decimal


class SimpleLoanCalculator(object):

    MIN_LOAN = 1000
    MAX_LOAN = 15000
    LOAN_BORROW_LENGTH_YEARS = 3

    def __init__(self, data_file, requested_loan):
        self.market_data_file = data_file
        self.file_handle = None
        self.requested_loan_amount = requested_loan

    def _is_requested_loan_amount_valid(self):
        """ Checks requested loan amount meets upper and lower limits of
        the loan system and is in increments of 100.
        """
        if (self.requested_loan_amount >= SimpleLoanCalculator.MIN_LOAN) \
                and (self.requested_loan_amount <= SimpleLoanCalculator.MAX_LOAN) \
                and self.requested_loan_amount % 100 == 0:
            return True
        else:
            raise ValueError(
                '>> Error: please request an amount between £{:,} and £{:,} '
                'in increments of 100!'.format(
                    SimpleLoanCalculator.MIN_LOAN, SimpleLoanCalculator.MAX_LOAN))

    def _check_file_exists(self):
        """ Checks if the data file passed as an argument to the class instance
        during instantiation actually exists, otherwise bail out of the program.
        """
        if os.path.isfile(os.path.abspath(self.market_data_file)):
            return True
        else:
            raise FileNotFoundError('>> Error: file "{}" not found!'.format(
                self.market_data_file))

    def _read_csv_file(self):
        """ Reads and returns a reader object which will iterate over lines in
        the given csv file and maps the column names.

        This method also checks if the csv file has any rows of data and
        that the number of columns are as expected.

        Manually close the file handle
        """
        self._check_file_exists()
        self._is_requested_loan_amount_valid()
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
            raise ValueError(
                '>> Error: file "{}" does not contain data!'.format(
                    self.market_data_file))
        else:
            return reader

    def _verify_number_of_columns_in_csv_file(self, csv_reader_obj):
        """ In the market lender data file, we expect 3 columns of data.
        """
        expected_columns = 3
        if len(csv_reader_obj.fieldnames) == expected_columns:
            return True
        else:
            raise ValueError(
                '>> Error: expected {} columns, but found {}!'.format(
                    expected_columns, len(csv_reader_obj.fieldnames)))

    def get_lowest_suitable_rate_from_lenders(self):
        reader = self._read_csv_file()

        # sort lenders by interest rate, converting it from string to decimal
        # and ordering it by lowest to highest
        sorted_list = sorted(
            reader, key=lambda row: Decimal(row['Rate']), reverse=False)
        self.file_handle.close()

        for lender in sorted_list:
            # requested loan is an int, because we are dealing with increments
            # of 100 and assume that the lender amount could be fractional,
            # therefore convert that to a decimal
            if self.requested_loan_amount <= Decimal(lender['Available']):
                return lender['Rate']
            else:
                continue
        return None

    def calculate_quote_using_monthly_compounding(self, interest_rate):
        """ This method calculates the new future amount based on
        monthly compounding interest.

        Returns:
            - the total future amount due
            - percentage annual interest
            - monthly repayment amount

        Using the formula :

        A = P (1 + r/n) ^ nt

        Where:

        A = the future amount, including interest
        P = the principal amount (the initial loan amount)
        r = the annual interest rate (decimal)
        n = the number of times that interest is compounded per year
        t = the number of years the money is borrowed for
        """
        P = Decimal(self.requested_loan_amount)
        r = Decimal(interest_rate)
        n = Decimal(12)
        t = Decimal(SimpleLoanCalculator.LOAN_BORROW_LENGTH_YEARS)

        A = P * (1 + (r / n)) ** (n * t)
        monthly_repayments = \
            A / (SimpleLoanCalculator.LOAN_BORROW_LENGTH_YEARS * 12)

        return round(A, 2), round(r * 100, 1), round(monthly_repayments, 2)
