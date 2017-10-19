#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from loan_calculator import SimpleLoanCalculator


def arg_parser():
    parser = argparse.ArgumentParser(
        description='For a requested loan amount, program displays a quota '
                    'based on the lowest annual interest rate from suitable '
                    'market lenders')
    parser.add_argument('csv_data_file', action="store", type=str,
                        help='market lender csv data file.')
    parser.add_argument('loan_amount', action="store", type=int,
                        help='loan amount in increments of 100')
    return parser.parse_args()


def main():
    args = arg_parser()

    loan_calc = SimpleLoanCalculator(args.csv_data_file, args.loan_amount)
    interest_rate = loan_calc.get_lowest_suitable_rate_from_lenders()

    # if a suitable interest rate for the requested loan is found then proceed
    # with a quote
    if interest_rate:
        new_principle, percentage_interest_rate, repayments = \
            loan_calc.calculate_quote_using_monthly_compounding(interest_rate)
        print('Requested amount: £{:,}'.format(args.loan_amount))
        print('Rate: {}%'.format(percentage_interest_rate))
        print('Monthly repayment: £{:,}'.format(repayments))
        print('Total repayment: £{:,}'.format(new_principle))
    else:
        print("Sorry, the system is unable to provide a quote at this time.")


if __name__ == '__main__':
    main()
