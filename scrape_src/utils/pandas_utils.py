# pandas
from pathlib import Path

import pandas as pd
from pandas.core.api import DataFrame


def pandas_configure():
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)


def classlist_to_dataframe(data, class_var_list, change_name_list=None) -> DataFrame:
    df = pd.DataFrame([{fn: getattr(f, fn) for fn in class_var_list} for f in data])
    if change_name_list is not None:
        df = df.set_axis(change_name_list, axis=1)

    return df


def print_dataframe(df: DataFrame):
    # set display rows and columns unlimited
    pandas_configure()
    print(df)


def save_dataframe_to_csv(df: DataFrame, filename):
    filepath = Path(f"result/csv/{filename}.csv")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath)


def save_dataframe_to_json(df: DataFrame, filename):
    filepath = Path(f"result/json/{filename}.json")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_json(filepath)
