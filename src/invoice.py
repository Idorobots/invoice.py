#! /bin/env python3

import argparse
import datetime
import json
import uuid
import pystache


def compute_amounts(data):
    for item in data['items']:
        net_amount = item['net_price'] * item['quantity']
        vat_amount = net_amount * item['vat']/100.0
        amount = net_amount + vat_amount
        item['net_amount'] = net_amount
        item['vat_amount'] = vat_amount
        item['amount'] = amount
    return data

def compute_totals(data):
    data['total_amount'] = sum([i['amount'] for i in data['items']])
    data['total_net_amount'] = sum([i['net_amount'] for i in data['items']])
    data['total_vat_amount'] = sum([i['vat_amount'] for i in data['items']])
    return data

def compute_tax_summary(data):
    data['taxes'] = []
    for l in reversed(list(set(sorted([i['vat'] for i in data['items']])))):
        items = [i for i in data['items'] if i['vat'] == l]
        data['taxes'].append(compute_totals({'vat': l, 'items': items}))
    return data

def process(data):
    d = compute_tax_summary(compute_totals(compute_amounts(data)))
    d['items'] = sorted(d['items'], key=lambda x: -x['amount'])
    return d

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
    p.add_argument('--number', '-n', help='consecutive number of the invoice')
    p.add_argument('--number-format', '-f', help='pystache format of the invoice number', default='{{year}}/{{month}}/{{number}}')
    p.add_argument('--template', '-t', help='selects invoice template')
    p.add_argument('--recipient', '-r', help='names the recipient of the invoice')
    p.add_argument('--currency', '-c', help='sets the currency of the invoice', default='PLN')
    p.add_argument('ITEMS', nargs='+', help='invoice items')

    args = p.parse_args()

    data = {
        'currency': args.currency,
        'date_of_sale': args.date_of_sale,
        'due_date': args.due_date,
        'invoice_template': args.template,
        'issuer': json.loads(args.issuer),
        'issue_date': args.issue_date,
        'items': list(map(json.loads, args.ITEMS)),
        'number': args.number,
        'number_format': args.number_format,
        'recipient': json.loads(args.recipient),
        'uuid': str(uuid.uuid4()),
        'year': d.strftime("%Y"),
        'month': d.strftime("%m"),
        'day': d.strftime("%d")
    }
    data['invoice_number'] = pystache.render(data['number_format'], **data)
    generate(process(data))
