class Currency(object):
    """this is the currency class"""

    # Currency class constructor
    def __init__(self, base, symbols, time):
        self.base = base
        self.symbols = symbols
        self.time = time