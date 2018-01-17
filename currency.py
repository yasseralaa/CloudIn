# python3
import sys
import datetime
import json
from urllib.request import urlopen
from pymongo import MongoClient
from currencyclass import Currency


def main():
    # Calling standard input library
    input = sys.stdin

    # Asking user to input base currency
    print("Enter Base Currency Code, Please.")

    # Receiving base currency code
    base_currency = str(input.readline().rstrip('\n'))

    # Asking user to input symbol currency codes separated by commas
    print("Enter Symbol Currency Codes Separated By Commas, Please.")

    # Receiving codes of the symbol currencies
    symbol_currencies = str(input.readline().rstrip('\n'))

    # Calling API executing method sending base and symbol currencies as parameters
    currency_data = get_data(base_currency, symbol_currencies)

    # Initializing currency object from Currency Class
    currency_object = Currency(base_currency, symbol_currencies.split(','),
                               currency_data['date'] + " " + datetime.datetime.now().strftime("%H:%M:%S"))

    # New string to make special format for DB
    symbols_db = ""

    # Iterating over every currency symbol code and make sure that it is supported
    for i, key in enumerate(currency_object.symbols):
        try:
            print("1 " + currency_object.base + " = " + str(currency_data['rates'][key]) + " " + key)
            symbols_db += key + ":" + str(currency_data['rates'][key])
            if i + 1 < len(currency_object.symbols):
                symbols_db += " "
        except:
            print(key + " : " + "We Do Not Support This Currency")

    # Create a new connection to a single MongoDB instance at host:port.
    connection = MongoClient()

    # Create and get a data base (db) from this connection
    db = connection.test

    # Create and get a collection named "currency" from the data base named "db" from the connection named "connection"
    collection = db.currency

    # Create an entry and insert in the collection
    entry = {"base": currency_object.base,
             "symbols": symbols_db,
             "date": currency_object.time}
    collection.insert(entry)

    # Print out the inserted entry
    print(list(collection.find()))

    # close connection
    connection.close()


def get_data(base, symbols):
    # Creating API link string
    api = "https://api.fixer.io/latest?base=" + base + "&symbols=" + symbols
    # Load API from the link and jsonify received data
    try:
        data = json.load(urlopen(api))
        return data
    except:
        print(base + " : " + "We Do Not Support This Currency")
        exit(0)


if __name__ == '__main__':
    main()
