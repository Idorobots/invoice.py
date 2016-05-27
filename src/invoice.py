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
    def date_to_str(d):
        return d.strftime("%Y-%m-%d")

    d = datetime.datetime.now()
    date = date_to_str(d)
    due = date_to_str(d + datetime.timedelta(days=14))

    p = argparse.ArgumentParser()
    p.add_argument('--date-of-sale', '-s', help='date of sale', default=date)
    p.add_argument('--due-date', help='payment due date', default=due)
    p.add_argument('--issuer', '-i', help='names the issuer of the invoice')
    p.add_argument('--issue-date', '-d', help='invoice issue date', default=date)
    p.add_argument('--number', '-n', help='names the number of the invoice')
    p.add_argument('--template', '-t', help='selects invoice template')
    p.add_argument('--recipient', '-r', help='names the recipient of the invoice')
    p.add_argument('ITEMS', nargs='+', help='invoice items')

    args = p.parse_args()

    generate({
        'date_of_sale': args.date_of_sale,
        'due_date': args.due_date,
        'invoice_number': args.number,
        'invoice_template': args.template,
        'issuer': json.loads(args.issuer),
        'issue_date': args.issue_date,
        'items': list(map(json.loads, args.ITEMS)),
        'recipient': json.loads(args.recipient),
        'uuid': str(uuid.uuid4())
    })
