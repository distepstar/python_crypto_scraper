from ..services import currencies_service as service


class CurrenciesController:
    @staticmethod
    def get_currency_overview(threads=4):
        service.get_currency_overview(threads)

    @staticmethod
    def get_currency_overview_dataframe():
        return service.get_currency_overview_dataframe()

    @staticmethod
    def get_sorted_currency_overview_dataframe(sorted_by="Name"):
        return service.get_sorted_currency_overview_dataframe(sorted_by)

    @staticmethod
    def print_currency_overview_dataframe(df):
        service.print_currency_overview_dataframe(df)

    @staticmethod
    def save_currency_overview(df, csv=True, json=True):
        service.save_currency_overview(df, csv, json)
