from typing import Literal

import numpy as np
import pandas as pd
import scipy.stats as stats


class StatisticalTests:
    _MAX_COLUMNS_CATEGORICAL_THRESHOLD = 20

    @classmethod
    def _is_categorical(cls, column_values: pd.Series):
        return len(column_values.unique()) > cls._MAX_COLUMNS_CATEGORICAL_THRESHOLD

    @classmethod
    def chi2_independence_between_columns(
        cls, column1_values: pd.Series, column2_values: pd.Series
    ):
        contingency_table = pd.crosstab(column1_values, column2_values)
        chi2, p_value, _, _ = stats.chi2_contingency(contingency_table)
        return chi2, p_value

    @classmethod
    def spearman_independence_between_columns(
        cls, column1_values: pd.Series, column2_values: pd.Series
    ):
        rho, p_value = stats.spearmanr(column1_values, column2_values)
        return rho, p_value

    @classmethod
    def independence_matrix(cls, df: pd.DataFrame):
        columns = df.columns
        len_columns = len(columns)
        matrix = np.zeros((len_columns, len_columns))

        categorical_columns = {}

        def is_categorical_memoized(column: str):
            if column in categorical_columns:
                return categorical_columns[column]
            is_categorical = cls._is_categorical(df[column])
            categorical_columns[i] = is_categorical
            return is_categorical

        for i in range(0, len_columns):
            for j in range(i, len_columns):
                if is_categorical_memoized(columns[i]) and is_categorical_memoized(
                    columns[j]
                ):
                    matrix[i][j] = cls.chi2_independence_between_columns(
                        df[columns[i]], df[columns[j]]
                    )[1]
                else:
                    matrix[i][j] = cls.spearman_independence_between_columns(
                        df[columns[i]], df[columns[j]]
                    )[1]
                matrix[j][i] = matrix[i][j]

        return pd.DataFrame(matrix, index=columns, columns=columns)

    @classmethod
    def correlation_matrix(
        cls,
        df: pd.DataFrame,
        method: Literal["pearson", "kendall", "spearman"] = "spearman",
    ):
        return df.corr(method=method)
