import pandas as pd
import matplotlib.pyplot as plt


def plot_data(file_path, x_column='A', y_column='B'):
    try:
        if file_path.endswith('.csv'):
            # Read CSV file
            df = pd.read_csv(file_path, error_bad_lines=False)
        elif file_path.endswith(('.xls', '.xlsx')):
            # Read Excel file
            df = pd.read_excel(file_path)
        else:
            print("Error: Unsupported file format. Please use CSV or Excel files.")
            return
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: No data found in '{file_path}'.")
        return
    except pd.errors.ParserError:
        print(f"Error: Issue with parsing data in '{file_path}'. Please check the file format.")
        return

    # Check for required columns
    print(df.columns)
    print(x_column, y_column)

    print(x_column in df.columns)
    print(y_column in df.columns)

    if x_column not in df.columns or y_column not in df.columns:
        print(f"Error: Data must have columns '{x_column}' and '{y_column}'.")
        return

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_column], df[y_column], marker='o', markersize=3, linestyle='-', color='b')
    plt.title('Data Plot')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.show()


# Example usage
file_path_csv = 'spx500.csv'
plot_data(file_path_csv)

