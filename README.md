A simple Python script to help Amazon sellers download FBA invoices, based on Amazon Seller Web API.

# Requirements

* `Python 3`
* `requests` Python module
* `argparse` Python module
* Amazon seller account (+ a session cookie)

# Example of usage

* Print the help:
```
$ python FBAInvoicesDL.py -h
usage: FBAInvoicesDL [-h] [-dl] cookie params

Get FBA invoices

positional arguments:
  cookie           Session cookie
  params           Search constraints (ex: limit=30&sort=order_date_desc)

options:
  -h, --help       show this help message and exit
  -dl, --download  Flag to enable download of invoices
```

* Download the 2 last ordered invoices:
```
$ python FBAInvoicesDL.py [your-sessin-cookie] "limit=2&sort=order_date_desc" -dl
------------- 403-1111111-2222222
https://sellercentral.amazon.fr/documents/download/aaaaaaaa-e9ee-4fff-aeee-832343737337/document.pdf
------------- 171-3333333-4444444
https://sellercentral.amazon.fr/documents/download/bbbbbbbb-e9ee-4fff-aeee-832343737337/document.pdf

------------- Summary: 2/2 invoices successfully found.

- Successfully found invoices iDs:
['403-1111111-2222222', '171-3333333-4444444']

- Errors encoutered for invoices IDs:
[]
$ ls
Invoice 403-1111111-2222222.pdf Invoice 171-3333333-4444444.pdf
```
* Other valid constraints: see Amazon Seller Web API documentation.
