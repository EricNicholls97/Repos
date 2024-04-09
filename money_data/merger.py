import pandas as pd
import glob


def combine_csvs(csv_files, output_file):
    # Initialize an empty DataFrame
    combined_data = pd.DataFrame()

    # Iterate through each CSV file and merge with combined_data
    for file in csv_files:
        print(f"Processing file: {file}")
        try:
            df = pd.read_csv(file, parse_dates=['date'],
                             date_parser=lambda x: pd.to_datetime(x, format='%m-%d-%Y', errors='coerce'))
            print("DataFrame from file:")
            print(df.head())  # Print first few rows of the DataFrame from the current file

            if combined_data.empty:
                combined_data = df
            else:
                combined_data = pd.merge(combined_data, df, on='date', how='outer')

        except Exception as e:
            print(f"Error processing file '{file}': {e}")

    # Sort by date
    combined_data.sort_values(by='date', inplace=True)
    combined_data.reset_index(drop=True, inplace=True)

    # Save the combined DataFrame to a CSV file
    combined_data.to_csv(output_file, index=False)
    print(f"Combined data saved to '{output_file}'")

    return combined_data


# Example usage
csv_files = glob.glob('*.csv')  # Assumes all CSV files are in the current directory
output_file = 'tmp/combined_data.csv'  # Output file name
combined_data = combine_csvs(csv_files, output_file)
print("Combined DataFrame:")
print(combined_data)
