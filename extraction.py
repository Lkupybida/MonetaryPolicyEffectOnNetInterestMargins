import os
import pandas as pd
import numpy as np
from datetime import datetime
import csv
from glob import glob

from pandas.tseries.offsets import DateOffset

# extract_bank_data('data/original/Aggregation', 'Фінрез', 'Чистий процентний дохід/(Чисті процентні витрати)', 'data/extracted/2018_to_now_monthly/')
# extract_bank_data('data/original/Aggregation', 'Фінрез', 'Чистий процентний дохід/(Чисті процентні витрати)', 'data/extracted/2018_to_now_monthly/')

def extract_bank_data(root_folder, sheet_name, column, file, name):
    target_banks = ["privatbank", "oschadbank", "ukreximbank", "ukrgasbank", "alfa", "sense", "first investment bank"]
    data = {}

    for year in range(2018, 2025):
        folder = os.path.join(root_folder, str(year))
        if not os.path.exists(folder):
            continue

        for file_name in os.listdir(folder):
            if file_name.endswith(".xlsx"):
                file_path = os.path.join(folder, file_name)
                try:
                    date = datetime.strptime(file_name[12:22], "%Y-%m-%d")
                except Exception as e:
                    print(f"Error reading {file_name}: {str(e)}")
                    continue
                try:
                    # Try reading with 4th row as header
                    df = pd.read_excel(file_path, sheet_name=sheet_name, header=3)
                    target_col = find_target_column(df, column)

                    # If target column not found, try with 5th row as header
                    if target_col is None:
                        df = pd.read_excel(file_path, sheet_name=sheet_name, header=4)
                        target_col = find_target_column(df, column)

                    if target_col is None:
                        print(f"Warning: Target column '{column}' not found in {file_name}")
                        continue

                    # print(date)

                except Exception as e:
                    print(f"Error reading {file_name}: {str(e)}")
                    continue

                for bank in range(1, 1000):
                    try:
                        bank_row = df[df['NKB'].astype(str).str.lower().str.contains(bank, case=False, na=False)]
                    except TypeError:
                        bank_str = str(bank)
                        # df['NKB'] = pd.to_numeric(df['NKB'], errors='coerce')
                        # df['NKB'] = df['NKB'].apply(lambda x: int(x) if pd.notna(x) else x)
                        # df['NKB'] = df['NKB'].dropna().astype(int)
                        bank_row = df[df['NKB'] == bank_str]
                    except Exception as e:
                        print(f"Error reading bank row at {date} {str(e)}")
                        continue
                    # bank_row = df[df['NKB'].astype(str).str.lower().str.contains(bank, case=False, na=False)]
                    if not bank_row.empty:
                        value = bank_row[target_col].values[0]
                        if date not in data:
                            data[date] = {}
                        data[date][bank] = value
                        # print(df['NKB'])
                    else:
                        bank_str = str(float(bank))
                        bank_row = df[df['NKB'] == bank]
                        # print(bank_row)
                        if not bank_row.empty:
                            value = bank_row[target_col].values[0]
                            # print(value)
                            if date not in data:
                                data[date] = {}
                            data[date][bank] = value
                        # print('bank_row is empty for ' + str(date))

    result_df = pd.DataFrame.from_dict(data, orient='index')
    result_df.index.name = 'Date'
    result_df.sort_index(inplace=True)

    output_file = file + name
    result_df.to_csv(output_file)
    result_df.index = pd.to_datetime(result_df.index)


    # Shift all dates one month back
    # result_df.index = result_df.index - DateOffset(months=1)
    print(f"Data extracted and saved to {output_file}")

def find_target_column(df, column):
    for col in df.columns:
        if isinstance(col, str) and column.lower() in col.lower():
            return col
    return None

def make_quarterly(path_to, name, path_from):
    df = pd.read_csv(path_to + name)
    df = df.rename(columns={df.columns[0]: 'date'})
    df.set_index(df.columns[0], inplace=True)
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    df_quarterly = df.resample('QE').sum()
    df_quarterly.index = pd.to_datetime(df_quarterly.index, format='%Y-%m')
    df_quarterly.to_csv(path_from + name)

def xlsx2csv(path_in, path_out):
    df = pd.read_excel(path_in, sheet_name=0)
    df.to_csv(path_out, index=False)

def remove_rolling_sum(file_path, out_path):
    df = pd.read_csv(file_path, index_col=0)
    df_diff = df.diff(axis=0)
    for idx in df.index:
        if datetime.strptime(idx, '%Y-%m-%d').month == 2:
            df_diff.loc[idx] = df.loc[idx]
    df_diff.to_csv(out_path)


# def divide(file1, file2, name):
#     df1 = pd.read_csv(file1)
#     df2 = pd.read_csv(file2)
#
#     df1["date"] = pd.to_datetime(df1["date"], format='%Y-%m-%d')
#     df1.set_index("date", inplace=True)
#     df2["date"] = pd.to_datetime(df2["date"], format='%Y-%m-%d')
#     df2.set_index("date", inplace=True)
#
#     for i in range(len(df1)):
#         for j in range(1, len(df1.columns)):
#             denominator = df2.iloc[i, j]
#             if denominator != 0:
#                 df1.iloc[i, j] = float(df1.iloc[i, j]) / float(denominator)
#             else:
#                 df1.iloc[i, j] = float('nan')  # Or use another placeholder for division by zero
#
#     df1.to_csv(name)

def divide(file1_path, file2_path, output_path):
    # Read the CSV files
    df1 = pd.read_csv(file1_path, index_col='date')
    df2 = pd.read_csv(file2_path, index_col='date')

    # Ensure the dataframes have the same shape
    if df1.shape != df2.shape:
        print(f'\nshape 1:\n', df1.shape, f'\nshape 2:\n', df2.shape)
        raise ValueError("The input CSV files must have the same shape.")


    # Perform element-wise division
    result = df1 / df2

    # Save the result to the output file
    result.to_csv(output_path)

def divide_csv_files(file1_path, file2_path):
    def read_csv(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Read and store headers
            data = []
            for row in reader:
                # Convert to float, use None for non-numeric values
                data.append([float(val) if val.replace('.','',1).isdigit() else None for val in row])
        return headers, data

    # Read both CSV files
    headers1, data1 = read_csv(file1_path)
    headers2, data2 = read_csv(file2_path)

    # Convert to numpy arrays for element-wise division
    arr1 = np.array(data1)
    arr2 = np.array(data2)

    # Perform element-wise division, handling None values
    result = np.divide(arr1, arr2, where=((arr2 != 0) & (arr1 != None) & (arr2 != None)))

    # Replace inf and nan values with None
    result = np.where(np.isinf(result) | np.isnan(result), None, result)

    return headers1, result.tolist()


def extract_unique_banks(directory_path):
    # List to store all bank names
    all_banks = []

    # Get all Excel files in the directory
    excel_files = glob(os.path.join(directory_path, '**', '*.xlsx', '*.xls'), recursive=True)

    # Loop through each Excel file
    for file in excel_files:
        # Read the Excel file
        try:
            df = pd.read_excel(file, header=3)
        except Exception as e:
            print(file)

        # Extract bank names from the third column (index 2)
        banks = df.iloc[:, 2].dropna().unique()

        # Add to the list of all banks
        all_banks.extend(banks)

    # Get unique bank names
    unique_banks = list(set(all_banks))

    # Create a DataFrame with unique bank names
    df_unique_banks = pd.DataFrame({'Bank Name': unique_banks})

    # Save to CSV
    output_file = os.path.join(directory_path, 'unique_banks.csv')
    df_unique_banks.to_csv(output_file, index=False)

    print(f"Unique bank names have been saved to {output_file}")

def get_value_from_excel(file_path, sheet_name, column_number, row_number):
    # Convert column and row numbers to integers
    try:
        column_number = int(column_number)
        row_number = int(row_number)
    except ValueError:
        return "Column number and row number must be integers"

    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Ensure the column and row numbers are within the DataFrame's bounds
    if column_number < 1 or column_number > df.shape[1]:
        return "Invalid column number"
    if row_number < 1 or row_number > df.shape[0]:
        return "Invalid row number"

    # Retrieve the value
    value = df.iloc[row_number - 1, column_number - 1]
    return value

def what_col_bank_data_starts(column, row):
    excel_files = glob(os.path.join('data/original/Aggregation', '**', '*.xlsx', '*.xls'), recursive=True)
    df = pd.DataFrame()
    dates = []
    values = []
    # Loop through each Excel file
    for file in excel_files:
        dates.append(file)
        values.append(get_value_from_excel(file, 1, column, row))
    df['dates'] = dates
    df['values'] = values
    df.to_csv('data/original/Aggregation/column' + str(column) + 'row' + str(row) + '.csv', index=False)

def ex():
    excel_files = glob(os.path.join('data/original/Aggregation', '**', '*.xlsx'), recursive=True)
    df = pd.DataFrame()
    df['files'] = excel_files
    df.to_csv('data/original/Aggregation/files.csv')