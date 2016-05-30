# invoice.py
A spartan invoice generator based on LaTeX and Pystache conforming to the Polish VAT invoice policy.

# Usage

```bash
/src/invoice.py --template "templates/basic.tex" \
                --number "1001" \
                --issuer $ISSUER \
                --recipient $RECIPIENT \
                $ITEM1 $ITEM2 $ITEM3
```

Where `$ISSUER` and `$RECIPIENT` take the following form:

```json
{
  "name" : "string, a name of a company",
  "address" : "string, an address of a company",
  "id" : "string, tax ID numbers of a company",
  "bank" : "optional string, the bank account number of a company",
  "extra" : "optional string, any extra info like phone numbers or URLs"
}
```

Each `$ITEM*` takes the following form:

```json
{
  "name" : "string, the name of an item or service",
  "net_price" : "number, the net price of an item or service",
  "quantity" : "number, quantity of the items/services",
  "quantity_unit" : "number, quantity unit",
  "vat" : "number, the VAT fee of an item or service[0-100]"
}
```

Additional values such as `item.amount`, `item.vat_amount` and `taxes` will be computed automatically and added to the mustache engine parameters before templating. You can supply any custom keys and values to any JSON object and use them in your templates.
