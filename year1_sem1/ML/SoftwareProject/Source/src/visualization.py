import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


class Visualization:
    FIG_SIZE = (15, 10)
    COLORS = [
        "red",
        "blue",
        "green",
        "brown",
        "yellow",
        "black",
        "magenta",
        "cyan",
        "lime",
        "orange",
    ]

    @classmethod
    def visualize_distributions(cls, df: pd.DataFrame, nrows: int, ncols: int):
        plt.figure(figsize=cls.FIG_SIZE)
        for idx, column in enumerate(df.columns, start=1):
            plt.subplot(
                nrows,
                ncols,
                idx,
            )
            plt.hist(df[column])
            plt.title(column)
        plt.tight_layout()
        plt.show()

    @classmethod
    def visualize_matrix_heatmap(
        cls, matrix: np.ndarray, title: str = None, exponential_notation: bool = False
    ):
        plt.figure(figsize=cls.FIG_SIZE)

        sns.heatmap(
            matrix,
            annot=True,
            fmt=".2e" if exponential_notation else ".2f",
            cmap="coolwarm",
            cbar=True,
            annot_kws={"size": 6} if exponential_notation else None,
        )
        if title:
            plt.title(title)
        plt.show()

    @classmethod
    def visualize_reduced_dataset(
        cls, features: np.ndarray, target: pd.Series, method_name: str | None = None
    ):
        classes = target.unique()

        if len(cls.COLORS) < len(classes):
            raise ValueError("Too many classes")

        colors = cls.COLORS[: len(classes)]

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.tick_params(axis="x", labelrotation=45)

        for idx, cls_label in enumerate(classes):
            indices = target == cls_label
            ax.scatter(
                features[indices, 0],
                features[indices, 1],
                c=colors[idx],
                label=str(cls_label),
            )

        ax.legend(loc="best")
        plt.xlabel(f"{method_name or ''} Component 1")
        plt.ylabel(f"{method_name or ''} Component 2")
        plt.title(f"{method_name or ''} Visualization of Dataset")
        plt.show()
