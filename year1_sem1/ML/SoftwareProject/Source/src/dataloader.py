import pandas as pd


class OccupancyEstimationDataloader:
    _TARGET_COLUMN = "Room_Occupancy_Count"

    def __init__(self, path: str, transform: callable = lambda x: x):
        self.dataframe = transform(pd.read_csv(path))
        self.input_columns = [
            column for column in self.dataframe.columns if column != self._TARGET_COLUMN
        ]
        self.output_column = self._TARGET_COLUMN        

    def __getitem__(self, idx: int):
        row = self.dataframe.iloc[idx]

        row_input = row[self.input_columns].to_dict()
        row_output = row[self.output_column]

        return row_input, row_output
        
    def __iter__(self):        
        for i in range(self.dataframe.shape[0]):
            yield self.__getitem__(i)

    def __len__(self):
        return len(self.dataframe)
