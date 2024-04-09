import pandas as pd

def convert_date_format(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Convert date column to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Convert date format from yyyy-mm-dd to mm-dd-yyyy
    df['date'] = df['date'].dt.strftime('%m-%d-%Y')

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    print(f"Conversion complete. New file saved as '{output_file}'")

# Example usage
input_file = 'tmp/spx500.csv'    # Replace 'input.csv' with the path to your input CSV file
output_file = 'tmp/spx500-2.csv'  # Specify the desired name for the output CSV file
convert_date_format(input_file, output_file)
