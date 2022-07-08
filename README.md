# HNTpayments
Generates CLI Multipayment JSON from CSV

## Overview

The Helium CLI wallet allows a user to send many payments in a single transaction by accepting
a JSON configuration file as a payment parameter. It looks something like the following:

`./helium-wallet -f {wallet.key} pay multi {paymentdata.json}`

...where `{wallet.key}` is the filename for the wallet keystore file you wish to pay from, and 
`{paymentdata.json}` is the [fully qualified] path for the payment data JSON config file.

## Setup & Use

To use this script, you will first need a .csv configuration file with each entry formatted as follows:

`Hotspot_Address, Payment_Address, Payment_Split`

...where `Hotspot_Address` is the hotspot being paid, `Payment_Address` is the wallet address
being paid, and `Payment Split` is a 2-decimal float value representing the percentage split (e.g. `0.50` for 50%).
You can reference [payment_details.csv](https://github.com/cvolkernick/HNTpayments/blob/master/payment_details.csv)
for an example template.

Once you have a properly configured csv file for payment splits, you can simply download `main.py` and 
[execute the script via command line](https://realpython.com/run-python-scripts/#how-to-run-python-scripts-using-the-command-line).
Provide the requested info at runtime, then copy / paste the output CLI multipayment command to issue the payment.

## Notes

Be advised that unless you remove the `--commit` from the output payment command, the payment will be issued on the blockchain.
You must remove the `--commit` flag to preview the payment transaction first.

It's also important to note that
the current maximum number of unique payment addresses for a CLI multipayment is `50`; if your payment splits csv input contains
more unique payment addresses than this, you may encounter errors trying to issue the payment the payment transaction
itself. If so, re-try with less per batch by splitting your csv file into multiple files.