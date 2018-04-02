#! /bin/env python3

import argparse
import datetime
import json
import pystache
import string
import uuid


def generate(data):
    with open(data['time_table_template'], 'r') as template:
        print(pystache.render(template.read(), **data))

if __name__ == "__main__":
    def date_to_str(d):
        return d.strftime("%Y-%m-%d")

    d = datetime.datetime.now()

    p = argparse.ArgumentParser()
    p.add_argument('--number', '-n', help='consecutive number of the invoice')
    p.add_argument('--number-format', '-f', help='pystache format of the invoice number', default='{{year}}/{{month}}/{{number}}')
    p.add_argument('--template', '-t', help='selects time table template')
    p.add_argument('--time-table-file', help='time table contents')
    p.add_argument('--uuid', '-u', help='a UUID for internal use', default=str(uuid.uuid4()))

    args = p.parse_args()

    data = {
        'time_table_template': args.template,
        'time_table_file': args.time_table_file,
        'number': args.number,
        'number_format': args.number_format,
        'uuid': args.uuid,
        'year': d.strftime("%Y"),
        'month': d.strftime("%m"),
        'day': d.strftime("%d")
    }
    data['invoice_number'] = pystache.render(data['number_format'], **data)
    generate(data)
