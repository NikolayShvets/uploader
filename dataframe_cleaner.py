import pandas as pd
import numpy as np


class Cleaner:
    @staticmethod
    def drop_duplicate_rows(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
        """

        :param df:
        :param subset:
        :return:
        """
        return df.drop_duplicates(subset=subset, inplace=True)

    @staticmethod
    def drop_duplicate_cols_by_name(df: pd.DataFrame) -> pd.DataFrame:
        """

        :param df:
        :return:
        """
        df = df.loc[:, ~df.columns.duplicated()]
        return df

    @staticmethod
    def drop_thrash_columns(df: pd.DataFrame, thrash_set: list) -> pd.DataFrame:
        """

        :param df:
        :param thrash_set:
        :return:
        """
        value = [np.NaN for i in range(len(thrash_set))]
        for column_name in df.columns:
            df[column_name].replace(thrash_set, value, inplace=True)
        return df

    @staticmethod
    def drop_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
        """

        :param df:
        :return:
        """
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
