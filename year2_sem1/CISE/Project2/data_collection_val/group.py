import os
import pandas as pd

def main():
    datasets_dir = "datasets"
    output_file = "data_grouped_raw.csv"

    all_rows = []

    for filename in os.listdir(datasets_dir):
        if filename.endswith(".csv"):
            repo = os.path.splitext(filename)[0]
            path = os.path.join(datasets_dir, filename)

            df = pd.read_csv(path)
            df.insert(0, "repo", repo)  # add 'repo' as first column
            all_rows.append(df)

    if not all_rows:
        print("No CSV files found in 'datasets'.")
        return

    final_df = pd.concat(all_rows, ignore_index=True)
    final_df.to_csv(output_file, index=False)
    print(f"✅ Merged {len(all_rows)} CSV files into '{output_file}'")

if __name__ == "__main__":
    main()
