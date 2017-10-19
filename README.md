# Loan Quota Coding Task

This program delivers a loan quota to stdout based on a given set of market data from lenders,
using monthly compounded interest for monthly repayments over a 3 year period.

# Execute program

Designed to run with standard Python 3 libraries

Usage:
```
$python3 ./get_quote.py -h                                
usage: get_quote.py [-h] csv_data_file loan_amount

For a requested loan amount, program displays a quota based on the lowest
annual interest rate from suitable market lenders

positional arguments:
  csv_data_file  market lender csv data file.
  loan_amount    loan amount in increments of 100

optional arguments:
  -h, --help     show this help message and exit
```

produces for example ...
```
$ python3 ./get_quote.py ./market_data.csv 5000                                                               
Requested amount: £5,000
Rate: 7.1%
Monthly repayment: £171.75
Total repayment: £6,183.04
```

## Tests

Unit-tests can be run as:
```
$ python3 ./test_loan_calculator.py
```
or
```
$ python3 -m unittest test_loan_calculator.TestLoanCalculatorDataValidation
$ python3 -m unittest test_loan_calculator.TestLoanCalculator
```
