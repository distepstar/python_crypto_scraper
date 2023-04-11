# threading
class CurrenciesOverview:
    currency_list = []
    fields = ["c_name", "c_price", "trend_state", "c_change", "c_volume", "c_marketcap"]

    def __init__(self, c_name, c_price, trend_state, c_change, c_volume, c_marketcap):
        self.c_name = c_name
        self.c_price = c_price
        self.trend_state = trend_state
        self.c_change = c_change
        self.c_volume = c_volume
        self.c_marketcap = c_marketcap

    def __str__(self):
        return f"CURRENCY: {self.c_name} || PRICE: {self.c_price} || TREND: {self.trend_state} || CHANGE IN 24h: {self.c_change} || VOLUME: {self.c_volume} || MARKET CAP: {self.c_marketcap}"
