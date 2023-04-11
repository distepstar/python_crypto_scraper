# controller
from scrape_src.controller.currencies_controller import CurrenciesController

# beautifulsoup_utils.prettier(doc)
# script_list = [item for item in doc.find_all("script") if "quoteName" in str(item)]
# script_list = script_list[0] if len(script_list) == 1 else script_list
# print(script_list)
# quoteAsset,

# currencies_json = json.loads(doc.text)
# json_utils.pretty_print(currencies_json, 4)


def main():
    # scraping currency overview
    CurrenciesController.get_currency_overview()
    # get currencies_df
    currencies_df = CurrenciesController.get_sorted_currency_overview_dataframe()
    # save currencies_df
    CurrenciesController.print_currency_overview_dataframe(currencies_df)
    CurrenciesController.save_currency_overview(currencies_df)


if __name__ == "__main__":
    main()
