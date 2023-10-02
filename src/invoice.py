#! /bin/env python3

import argparse
import datetime
import json
import pystache
import string
import uuid

DATE_FORMAT = "%Y-%m-%d"


def compute_amounts(data):
    rate = data['exchange_rate']
    for item in data['items']:
        vat = item['vat']
        if type(item['vat']) == str:
            vat = 0
        net_amount = item['net_price'] * item['quantity']
        vat_amount = net_amount * vat / 100.0
        amount = net_amount + vat_amount
        item['net_amount'] = net_amount
        item['vat_amount'] = vat_amount
        item['amount'] = amount
        item['net_price_local'] = item['net_price'] * rate
        item['net_amount_local'] = net_amount * rate
        item['vat_amount_local'] = vat_amount * rate
        item['amount_local'] = amount * rate
    return data

def compute_totals(data):
    data['total_amount'] = sum([i['amount'] for i in data['items']])
    data['total_net_amount'] = sum([i['net_amount'] for i in data['items']])
    data['total_vat_amount'] = sum([i['vat_amount'] for i in data['items']])
    rate = data['exchange_rate']
    data['total_amount_local'] = data['total_amount'] * rate
    data['total_net_amount_local'] = data['total_net_amount'] * rate
    data['total_vat_amount_local'] = data['total_vat_amount'] * rate
    return data

def compute_tax_summary(data):
    data['taxes'] = []
    for l in reversed(list(set(sorted([i['vat'] for i in data['items']])))):
        items = [i for i in data['items'] if i['vat'] == l]
        data['taxes'].append(compute_totals({
            'vat': l,
            'items': items,
            'exchange_rate': data['exchange_rate']
        }))
    return data

def maybe_stringify(key, value):
    if 'amount' in key or 'price' in key:
        return '{:.2f}'.format(value)
    else:
        return stringify_amounts(value)

def stringify_amounts(data):
    if type(data) == type({}):
         return {k: maybe_stringify(k, v) for k, v in data.items()}
    elif type(data) == type([]):
        return [stringify_amounts(v) for v in data]
    else:
        return data

def process(data):
    d = compute_tax_summary(compute_totals(compute_amounts(data)))
    d['items'] = sorted(d['items'], key=lambda x: -x['amount'])
    return stringify_amounts(d)

def generate(data):
    with open(data['invoice_template'], 'r') as template:
        print(pystache.render(template.read(), **data))

if __name__ == "__main__":
    def date_to_str(d):
        return d.strftime(DATE_FORMAT)

    default = datetime.datetime.now()
    default_date = date_to_str(default)
    default_due = date_to_str(default + datetime.timedelta(days=14))
    default_exchange = date_to_str(default - datetime.timedelta(days=1))

    p = argparse.ArgumentParser()
    p.add_argument('--currency', '-c', help='sets the currency of the invoice', default='PLN')
    p.add_argument('--currency-local', help='sets the local currency of the invoice', default='PLN')
    p.add_argument('--date-of-sale', '-s', help='date of sale', default=default_date)
    p.add_argument('--due-date', help='payment due date', default=default_due)
    p.add_argument('--exchange-rate', '-e', help="exchange rate of the currencies", default="1.0")
    p.add_argument('--exchange-rate-date', help="date of the exchange rate", default=default_exchange)
    p.add_argument('--issuer', '-i', help='names the issuer of the invoice')
    p.add_argument('--issue-date', '-d', help='invoice issue date', default=default_date)
    p.add_argument('--number', '-n', help='consecutive number of the invoice')
    p.add_argument('--number-format', '-f', help='pystache format of the invoice number', default='{{year}}/{{month}}/{{number}}')
    p.add_argument('--template', '-t', help='selects invoice template')
    p.add_argument('--recipient', '-r', help='names the recipient of the invoice')
    p.add_argument('--uuid', '-u', help='a UUID for internal use', default=str(uuid.uuid4()))
    p.add_argument('ITEMS', nargs='+', help='invoice items')

    args = p.parse_args()

    d = datetime.datetime.strptime(args.date_of_sale, DATE_FORMAT)

    data = {
        'currency': args.currency,
        'currency_local': args.currency_local,
        'date_of_sale': args.date_of_sale,
        'due_date': args.due_date,
        'exchange_rate': float(args.exchange_rate),
        'exchange_rate_date': args.exchange_rate_date,
        'invoice_template': args.template,
        'issuer': json.loads(args.issuer),
        'issue_date': args.issue_date,
        'items': list(map(json.loads, args.ITEMS)),
        'number': args.number,
        'number_format': args.number_format,
        'recipient': json.loads(args.recipient),
        'uuid': args.uuid,
        'year': d.strftime("%Y"),
        'month': d.strftime("%m"),
        'day': d.strftime("%d")
    }
    data['invoice_number'] = pystache.render(data['number_format'], **data)
    generate(process(data))
