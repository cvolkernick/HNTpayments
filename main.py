import requests
import json
import csv

def hotspot_earnings(address, start, end):
    # Get a hotspot's earnings for the specified range

    endpoint = 'https://api.helium.io/v1/hotspots/' + address + '/rewards/sum?min_time=' + start + '&max_time=' + end
    response = requests.get(endpoint)
    status = response.status_code

    if status != 200:
        while status != 200:
            response = requests.get(endpoint)
            status = response.status_code

    content = response.content
    json_content = json.loads(content)
    earnings = json_content['data']['total']

    return earnings

def parse_payments(csvfile, start, end):

    payments = {}

    with open(csvfile, 'r') as payment_details:

        reader = csv.reader(payment_details, delimiter=',')

        for row in reader:

            hotspot_address = str(row[0])
            payment_address = str(row[1])
            payment_split = float(row[2])

            rewards = hotspot_earnings(hotspot_address, start, end)
            earnings = rewards * payment_split

            if payment_address in payments.keys():

                payments[payment_address] = round(payments[payment_address] + earnings, 8)

            else:
                payments[payment_address] = round(earnings, 8)

    return payments

def print_payments(payments, start, end):

    for payment in payments:
        print('{} earned {:.8f} HNT for dates {} through {}'.format(payment, payments[payment], start, end))

def create_json(payments):

    file = open('paymentdata.json', 'w')
    json_items = []

    for payment in payments:

        if payments[payment] != 0:
            json_string = '{ "address": ' + '"{}", '.format(payment) + '"amount": ' + '{}'.format(payments[payment]) + ' }'
            json_object = json.loads(json_string)
            json_items.append(json_object)

    json_contents = json.dumps(json_items)

    file.write(json_contents)
    file.close()

def gather_input():

    print('This script will use a specified .csv file, with each line in the following format:')
    print('')
    print('Hotspot_Address, Payment_Address, Payment_Split')
    print('')
    print('...where payment split percentage is represented as a 2 decimal float.')
    print('')
    print('Example: 123, abcxyz, 0.50')
    print('')
    print('')
    print('Enter the date range for the period you would like to pay.')
    print('Start date is inclusive. End date is exclusive.')
    print('Example: Full month of January 2022 is 2022-01-01 through 2022-02-01')
    print('')

    start = input('Start Date (YYYY-MM-DD): ')
    end = input('End Date (YYYY-MM-DD): ')
    csvfile = input('Payment splits CSV [fully qualified] file path: ')
    jsonfile = input('Multipayment JSON output [fully qualified] file path: ')
    key = input('Wallet keystore file to use: ')



    results = {'start': start, 'end': end, 'csvfile': csvfile, 'jsonfile': jsonfile, 'key': key}

    return results

def run():

    input_data = gather_input()

    start = input_data['start']
    end = input_data['end']
    csvfile = input_data['csvfile']
    jsonfile = input_data['jsonfile']
    key = input_data['key']

    payments = parse_payments(csvfile, start, end)
    print_payments(payments, start, end)
    create_json(payments)

    multipayment_command = './helium-wallet -f {} pay multi --commit {}'.format(key, jsonfile)
    print(multipayment_command)

if __name__ == '__main__':
    run()