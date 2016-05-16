#! /bin/env python3

import argparse
import datetime
import json
import uuid
import pystache


def generate(data):
    with open(data['invoice_template'], 'r') as template:
        print(pystache.render(template.read(), **data))

if __name__ == "__main__":
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    p = argparse.ArgumentParser()
    p.add_argument('--date-of-sale', '-s', help='date of sale', default=date)
    p.add_argument('--issuer', '-i', help='names the issuer of the invoice')
    p.add_argument('--issue-date', '-d', help='invoice issue date', default=date)
    p.add_argument('--number', '-n', help='names the number of the invoice')
    p.add_argument('--template', '-t', help='selects invoice template')
    p.add_argument('--recipient', '-r', help='names the recipient of the invoice')
    p.add_argument('ITEMS', nargs='+', help='invoice items')
    args = p.parse_args()

    generate({
        'date_of_sale': args.date_of_sale,
        'invoice_number': args.number,
        'invoice_template': args.template,
        'issuer': args.issuer,
        'issue_date': args.issue_date,
        'items': list(map(json.loads, args.ITEMS)),
        'recipient': args.recipient,
        'uuid': str(uuid.uuid4())
    })
