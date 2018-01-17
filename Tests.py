import json
import unittest
from urllib.request import urlopen


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

class TestApi(unittest.TestCase):
    """this is the TestApi class"""

    def test_success1(self):
        self.assertEqual(get_data("EUR", "USD"),
                         {'base': 'EUR', 'date': '2018-01-16', 'rates': {'USD': 1.223}})

    def test_success2(self):
        self.assertEqual(get_data("USD", "EGP"),
                         {'base': 'USD', 'date': '2018-01-16', 'rates': {}})

    def test_success3(self):
        self.assertEqual(get_data("USD", "EGP,EUR"),
                         {'base': 'USD', 'date': '2018-01-16', 'rates': {'EUR': 0.81766}})

    def test_fail1(self):
        self.assertNotEqual(get_data("EUR", "USD"),
                         {'base': 'EUR', 'date': '2018-01-16', 'rates': {'BGN': 1.223}})

    def test_fail2(self):
        self.assertNotEqual(get_data("USD", "EGP"),
                         {'base': 'USD', 'date': '2018-01-16', 'rates': {'EGP': 18.001}})

    def test_fail3(self):
        self.assertNotEqual(get_data("USD", "EGP,EUR"),
                         {'base': 'USD', 'date': '2018-01-16', 'rates': {'EGP': 18.001, 'EUR': 0.81766}})


if __name__ == '__main__':
    unittest.main()
