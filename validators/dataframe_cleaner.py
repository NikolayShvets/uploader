import pandas as pd
import numpy as np
from typing import List


class Cleaner:
    @staticmethod
    def drop_duplicate_rows(df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """

        :param df:
        :param subset:
        :return:
        """

        df = df.copy()
        df.drop_duplicates(subset=subset, inplace=True)
        return df

    @staticmethod
    def drop_duplicate_cols_by_name(df: pd.DataFrame) -> pd.DataFrame:
        """

        :param df:
        :return:
        """

        df = df.copy()
        df = df.loc[:, ~df.columns.duplicated()]
        return df

    @staticmethod
    def drop_thrash_columns(df: pd.DataFrame, thrash_set: list) -> pd.DataFrame:
        """

        :param df:
        :param thrash_set:
        :return:
        """

        df = df.copy()
        df.replace(to_replace="\s{2,}", value=np.NaN, regex=True, inplace=True)
        value = [np.NaN for i in range(len(thrash_set))]
        df.replace(thrash_set, value, inplace=True)
        df.dropna(how="all", inplace=True)
        df.dropna(axis=1, how="all", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    @staticmethod
    def drop_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
        """

        :param df:
        :return:
        """

        df = df.copy()
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df

    @staticmethod
    def drop_nulls(df: pd.DataFrame):
        df = df.copy()
