import datetime
from abc import ABC, abstractmethod

import pandas as pd


class BaseProcessor(ABC):
    @classmethod
    @abstractmethod
    def process(cls, df: pd.DataFrame): ...


class DateAndTimePreprocessor(BaseProcessor):
    _DATE_COLUMN = "Date"
    _TIME_COLUMN = "Time"
    _TARGET_COLUMN = "Room_Occupancy_Count"
    _TIMES_DIVISIONS = [6, 9, 12, 14, 17, 19, 22]

    @classmethod
    def _drop_unoccupied_dates(cls, df: pd.DataFrame):
        dates = set(df[cls._DATE_COLUMN])
        unoccupied_dates = []
        for date in dates:
            room_occupancies = set(df[df[cls._DATE_COLUMN] == date][cls._TARGET_COLUMN])
            if len(room_occupancies) == 1:
                unoccupied_dates.append(date)

        return df[~df[cls._DATE_COLUMN].isin(unoccupied_dates)]

    @classmethod
    def _preprocess_date(cls, date_column: pd.Series):
        date_mapping = {date: idx + 1 for idx, date in enumerate(date_column.unique())}
        return date_column.map(date_mapping)

    @classmethod
    def _categorize_time(cls, time: datetime.time):
        for idx, time_division in enumerate(cls._TIMES_DIVISIONS, start=1):
            if time.hour < time_division:
                return idx
        return len(cls._TIMES_DIVISIONS)

    @classmethod
    def _preprocess_time(cls, time_column: pd.Series):
        time_column = pd.to_datetime(
            time_column, format="%H:%M:%S", errors="coerce"
        ).dt.time

        return time_column.apply(cls._categorize_time)

    @classmethod
    def process(cls, df: pd.DataFrame):
        df = cls._drop_unoccupied_dates(df)
        df[cls._DATE_COLUMN] = cls._preprocess_date(df[cls._DATE_COLUMN])
        df[cls._TIME_COLUMN] = cls._preprocess_time(df[cls._TIME_COLUMN])
        return df
