import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from colorama import Fore, Style, init
import logging
import random
from matplotlib.ticker import FuncFormatter
from decimal import Decimal, InvalidOperation

from pandas.tseries.offsets import DateOffset
import openpyxl
import geopandas as gpd
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.font_manager import FontProperties
from matplotlib.patheffects import withStroke
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Tuple, Dict, Union
import colorsys
import seaborn as sns
from matplotlib.sankey import Sankey
import holoviews as hv
import hvplot.pandas
from holoviews import opts
from matplotlib.ticker import FuncFormatter
import csv
from glob import glob
import re
import sys
from contextlib import contextmanager

def find_all_excel_paths():
    excel_files = glob(os.path.join('data/original/Aggregation', '**', '*.xlsx'), recursive=True)
    exel_files = glob(os.path.join('data/original/Aggregation', '**', '*.xls'), recursive=True)
    files = excel_files + exel_files
    excel_filenames = [os.path.splitext(os.path.basename(file))[0] for file in excel_files]
    exel_filenames = [os.path.splitext(os.path.basename(file))[0] for file in exel_files]
    df = pd.DataFrame()
    result = excel_filenames + exel_filenames
    result2 = []
    for file in result:
        if file.startswith("aggregation_") == True:
            new_filename = file[len("aggregation_"):]
            result2.append(new_filename)
        else:
            result2.append(file)
    result3 = []
    for file in result2:
        try:
            date = datetime.strptime(file, "%Y-%m-%d")
        except:
            try:
                date = datetime.strptime(file, "%d%m%Y")
            except:
                try:
                    date = datetime.strptime(file, "%Y%m%d")
                except Exception as e:
                    print(f"Error reading {file}: {str(e)}")
                    continue
        result3.append(date)
    # values3_5 = []
    values4_8 = []
    values3_7 = []
    values4_7 = []
    values4_11 = []
    values4_6 = []
    values3_6 = []
    # Loop through each Excel file
    # for file in files:
    #     values3_5.append(get_value_from_excel(file, 1, 3, 4))
    df['dates'] = result3
    df['dates'] = pd.to_datetime(df['dates'])
    # df['values3_5'] = values3_5

    df['files'] = files
    df.sort_values(by='dates', inplace=True)

    df.to_csv('data/original/Aggregation/files.csv', index=False)


def get_value_from_excel(file_path, sheet_name, column_number, row_number):
    # Convert column and row numbers to integers
    try:
        column_number = int(column_number)
        row_number = int(row_number)
    except ValueError:
        return "Column number and row number must be integers"
    if file_path in ['data/original/Aggregation/2016/20160701.xlsx', 'data/original/Aggregation/2017/20170401.xlsx', 'data/original/Aggregation/2017/20170701.xlsx', 'data/original/Aggregation/2017/20171001.xlsx']:
        df = pd.read_excel(file_path, sheet_name='Активи банків')
        # print(file_path, df)
    else:
        # Read the Excel file
        df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Ensure the column and row numbers are within the DataFrame's bounds
    if column_number < 1 or column_number > df.shape[1]:
        # print('column number: ', column_number, '\n df shape: ', df.shape[1], '\n df: ', df)
        return "Invalid column number"
    if row_number < 1 or row_number > df.shape[0]:
        return "Invalid row number"

    # Retrieve the value
    value = df.iloc[row_number - 1, column_number - 1]
    return value

def what_col_bank_data_starts(column, row):
    excel_files = glob(os.path.join('data/original/Aggregation', '**', '*.xlsx'), recursive=True)
    exel_files = glob(os.path.join('data/original/Aggregation', '**', '*.xls'), recursive=True)
    files = excel_files + exel_files
    df = pd.DataFrame()
    dates = []
    values = []
    # Loop through each Excel file
    for file in files:
        dates.append(file)
        values.append(get_value_from_excel(file, 1, column, row))
    df['dates'] = dates
    df['values'] = values
    df.to_csv('data/original/Aggregation/column' + str(column) + 'row' + str(row) + '.csv', index=False)


def extract_unique_banks(directory_path):
    # List to store all bank names
    all_banks = []

    # Get all Excel files in the directory
    excel_files = glob(os.path.join('data/original/Aggregation', '**', '*.xlsx'), recursive=True)
    exel_files = glob(os.path.join('data/original/Aggregation', '**', '*.xls'), recursive=True)
    files = excel_files + exel_files

    # Loop through each Excel file
    for file in files:
        banks = []
        # Read the Excel file
        try:
            for i in range(1, 200):
                value = get_value_from_excel(file, 1, 3, i+5)
                banks.append(value)
                # if i == 1:
                    # print('value: ', value)
        except Exception as e:
            print(file)

        # Extract bank names from the third column (index 2)
        # banks = df.iloc[:, 2].dropna().unique()

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

from col_names import *

def extract_bank_data(sheet_name, column, output_file):
    if sheet_name == 'Assets':
        sheet_name = 0
    elif sheet_name == 'Liabilities':
        sheet_name = 1
    elif sheet_name == 'Capital':
        sheet_name = 2
    elif sheet_name == 'Finresults':
        sheet_name = 3
    else:
        print('Incorrect sheet name: ', sheet_name)
        return
    sheet_names = [['Активи', 'Активи банків', ' Активи банків', 'Активи'],
                   ['Зобовязання', "Зобов'язання банків", "Зобов`язання"],
                   ['Власний капітал', 'Капітал банків', 'Капітал', 'Власний капітал банків', ' Капітал банків', 'Капітал '],
                   ['Фінансові результати', 'Фінансові результати банків', 'Фінрез'],
                   ['Money']]
    sheet = sheet_names[sheet_name]
    data = {}
    files_path = 'data/original/Aggregation/files.csv'
    files_df = pd.read_csv(files_path)

    for file_num in range(0, len(files_df['dates'])):
        date = files_df['dates'][file_num]
        file_path = files_df['files'][file_num]
        df = None
        for sheet_name in sheet:
            try:
                target_col, df = find_target_column_wrapper(file_path, sheet_name, column, date)
                # print(df[target_col])
                # print(f"Successfully read sheet '{sheet_name}' for date {date}")
                break
            except Exception as e:
                # print(f"Error reading sheet '{sheet_name}' in file for {date}: {str(e)}")
                ok =2

        # if date in ['2018-01-01','2018-02-01','2018-03-01']:
        #     if column in [cash, securities1, securities2]:
        #         if column in [securities1, securities2]:
        #             if date == '2018-01-01':
        #                 df.to_csv('data/extracted/check.csv')
        #                 ok =1
        #         # print(f"Shape of DataFrame for {date}: {df.shape}")
        #         # print(f"Columns in DataFrame: {df.columns.tolist()}")
        #         # print(f"Target column: {target_col}")
        #         # df = df.set_index('Банк')
        #         # print(f"First few rows of DataFrame:\n{df.head()}")
        #         # df.drop(column='Unnamed: 1')
        #         # print(df.columns)
        #         ok =1
        #         # df.to_csv('data/extracted/check.csv')
        #     else:
        #         # print(f"Shape of DataFrame for {date}: {df.shape}")
        #         # print(f"Columns in DataFrame: {df.columns.tolist()}")
        #         # print(f"Target column: {target_col}")
        #         # print(f"First few rows of DataFrame:\n{df.head()}")
        #         df = df.set_index(find_target_column(df, 'Банк'))
        #         # df.to_csv('data/extracted/check.csv')

        if date in ['2011-10-01']:
            if sheet_name != 'Власний капітал':
                # print('target: ', find_target_column(df, 'Назва Банку'))
                df.reset_index()
                # print('target: ', find_target_column(df, 'Назва Банку'))
                df = df.set_index(find_target_column(df, 'Назва банку'))
                # print(f"Shape of DataFrame for {date}: {df.shape}")
                # print(f"Columns in DataFrame: {df.columns.tolist()}")
                # print(f"Target column: {target_col}")
                # print(f"First few rows of DataFrame:\n{df.head()}")
                # df.to_csv('data/extracted/check.csv')
        # print(date)


        # if date in ['2018-01-01','2018-02-01','2018-03-01']:
        #     # print('first if passed')
        #     date_data = {}
        #     for bank_name, row in df.iterrows():
        #         # print(bank_name, row)
        #         if isinstance(bank_name, str):
        #             # print('first if passed')
        #             if bank_name != 'Банк':  # Skip the header row
        #                 # print('second if passed')
        #                 renamed_bank = rename_bank(bank_name)
        #                 if renamed_bank != "Error":
        #                     try:
        #                         value = row[target_col]
        #                         if pd.notna(value):
        #                             date_data[renamed_bank] = value
        #                             # print(f"Added data for {renamed_bank}: {value}")
        #                         # else:
        #                         # print(f"Skipping NaN value for {renamed_bank}")
        #                     except KeyError:
        #                         ok = 1

        if df is None:
            print(f"Couldn't read any sheet for date {date} Sheet: {sheet}")
            continue

        else:
            # Rename banks and extract data
            date_data = {}
            for bank_name, row in df.iterrows():
                if isinstance(bank_name, str) and bank_name != 'Назва банку':  # Skip the header row
                    renamed_bank = rename_bank(bank_name)
                    if renamed_bank != "Error":
                        try:
                            value = row[target_col]
                            if pd.notna(value):
                                date_data[renamed_bank] = value
                                # print(f"Added data for {renamed_bank}: {value}")
                            # else:
                                # print(f"Skipping NaN value for {renamed_bank}")
                        except KeyError:
                            ok = 1
                            # print(f"Column {target_col} not found in file for {date}")
                    # else:
                        # print(f"Skipping invalid bank name: {bank_name}")
                # else:
                    # print(f"Skipping non-string bank name or header: {bank_name}")

        if date_data:
            data[date] = date_data
            # if date in ['2018-01-01','2018-02-01','2018-03-01']:
            #     ok = 1
            #     print(f"Added data for {len(date_data)} banks on {date}")
        else:
            print(f"No valid data found for date {date}")
            # print(df)
            # df.to_csv('data/extracted/check.csv')

    if not data:
        print("No data was extracted. Check the input files and column names.")
        return

    # Create DataFrame from the collected data
    result_df = pd.DataFrame.from_dict(data, orient='index')
    result_df.index.name = 'Date'
    result_df.sort_index(inplace=True)

    # Convert index to datetime
    result_df.index = pd.to_datetime(result_df.index)

    # Save the result to CSV
    result_df.to_csv(output_file)
    print(f"Data extracted and saved to {output_file}")
    print(f"Extracted data for {len(result_df.columns)} banks over {len(result_df)} dates")
    print(result_df.head())

def find_target_column(df, column):
    for col in df.columns:
        if col == 'Чистий комісійний дохід/(Чисті комісійні витрати)':
            continue
        if isinstance(col, str) and column.lower() in col.lower():
            return col
    return None

def find_target_column_wrapper(file_path, sheet_name, column, date):
    # Try reading with 4th row as header
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=0, index_col=2)
    target_col = ''
    for col in column:
        target_col = find_target_column(df, col)
        # df.to_csv('data/extracted/check.csv')
        # If target column is found, break the loop
        if target_col is not None:
            # print(df[target_col])
            break

        # If target column not found, try with different rows as header
        for header_row in range(1, 6):
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row, index_col=2)
            target_col = find_target_column(df, col)
            if target_col is not None:
                # print(df[target_col])
                break

        # If target column is still not found after trying all headers
    if target_col is None:
        if date in ['2009-04-01', '2009-07-01', '2009-10-01', '2010-01-01', '2010-04-01', '2010-07-01', '2010-10-01',
                    '2011-01-01', '2011-04-01', '2011-07-01', '2012-01-01', '2012-04-01', '2012-07-01']:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=2, index_col=2)
            target_col = find_target_column(df, col)
            # print('df found:', df, target_col)
            # df.to_csv('data/extracted/check.csv')
            # if date.startswith('2018'):
            #     print('\n\nDate: ', date, 'Column looked for: ', col, '\nColumn found: ', target_col)
            return target_col, df
        if date in ['2011-10-01']:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=2, index_col=0)
            # print('hheeeeeeeeeeeelp', df)
            target_col = find_target_column(df, col)
            # print('df found:', df, target_col)
            # df.to_csv('data/extracted/check.csv')
            # if date.startswith('2018'):
            #     print('\n\nDate: ', date, 'Column looked for: ', col, '\nColumn found: ', target_col)
            return target_col, df
        if date in ['2018-01-01', '2018-02-01', '2018-03-01']:
            ok=1
        #     df = pd.read_excel(file_path, sheet_name=5, header=4, index_col=1)
        # #     # print('hheeeeeeeeeeeelp', df)
        #     target_col = find_target_column(df, col)
        #     # if target_col is None:
        #     #     print(df[col])
        #     print('target col found:', target_col)
        #     #
        #     # df.to_csv('data/extracted/check.csv')
        #     return target_col, df

        print(f"Warning: Target column '{col}' not found in {date}")
    # if date.startswith('2018'):
    #     print('\n\nDate: ', date, 'Column looked for: ', col, '\nColumn found: ', target_col)
    return target_col, df

def rename_bank(bank_name, csv_file_path='data/original/Aggregation/more_unique_banks.csv'):
    if not isinstance(bank_name, str):
        return "Error"
    # Ambiguous names list
    ambiguous_names_list = [
        ["ФІНБАНК", "ПРОФІНБАНК"],
        ["ТРАСТ", "ТРАСТ-КАПІТАЛ", "ІНВЕСТИЦІЙНО-ТРАСТ.БАНК"],
        ["КИЇВ", "КИЇВСЬКА РУСЬ", "СТАРОКИЇВСЬКИЙ БАНК"],
        ["МЕГА БАНК", "ОМЕГА БАНК"],
        ["ЦЕНТР", "РОЗРАХУНКОВИЙ ЦЕНТР"],
        ["СХІДНОЄВРОПЕЙСЬКИЙ БАНК", "ЄВРОПЕЙСЬКИЙ БАНК РАЦІОН.ФІНАНС.", "ЄВРОПЕЙСЬКИЙ"],
        ["КАПІТАЛ", "БАНК НАРОДНИЙ КАПІТАЛ", "БАНК РЕНЕСАНС КАПІТАЛ", "БАНК УКРАЇНСЬКИЙ КАПІТАЛ", "ЗЕМЕЛЬНИЙ КАПІТАЛ",
         "ТРАСТ-КАПІТАЛ"],
        ["СТАНДАРТ", "БІЗНЕС СТАНДАРТ", "БАНК РУСКИЙ СТАНДАРТ"],
        ["А - БАНК", "ПОЛТАВА - БАНК"],
        ["СОЮЗ", "ФІНАНСОВИЙ СОЮЗ БАНК"]
    ]

    # Create ambiguous names dictionary
    ambiguous_names = {}
    for group in ambiguous_names_list:
        for name in group:
            ambiguous_names[name.lower()] = group

    # Read the CSV file and create a lowercase dictionary
    bank_dict = {}
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            official_name = row[0]
            lowercase_names = [name.lower() for name in row]
            bank_dict[official_name] = lowercase_names

    # Convert input bank name to lowercase
    bank_name_lower = bank_name.lower()

    # Check if the bank name is in the ambiguous list
    for amb_name, full_names in ambiguous_names.items():
        if amb_name in bank_name_lower:
            # If it's ambiguous, we need to check for a more specific match
            for full_name in full_names:
                if full_name.lower() in bank_name_lower:
                    return full_name
            # If no specific match found, return the original ambiguous name
            return bank_name

    # Check for matches in the main dictionary
    for official_name, lowercase_names in bank_dict.items():
        if any(name in bank_name_lower for name in lowercase_names):
            return official_name

    # If no match is found, return the original bank name
    return "Error"

def quartalize_and_differ_wrapper(file, differ = False, expenses=False):
    path = 'data/extracted/mixed/'
    split_csv_at_time(path + file, '2018-01-01', 'Date','data/extracted/2009_to_2017_quaterly/' + file, 'data/extracted/2018_to_now_monthly/' + file)

    if expenses:
        twentyeghtieenOone = extract_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2018-01-01')
        twenty1704 = extract_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2017-04-01')
        twenty1707 = extract_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2017-07-01')
        twenty1710 = extract_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2017-10-01')

        correction = multiply_elements_except_first(twentyeghtieenOone)

        correction2 = apply_operation(correction, twenty1704, twenty1707, twenty1710)

        update_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2018-01-01', correction2)
        multiply_data_by_negative_one('data/extracted/2009_to_2017_quaterly/' + file)

    make_quarterly('data/extracted/2018_to_now_monthly/' + file, 'data/extracted/2018_to_now_quaterly/' + file)

    add_one_day_to_dates('data/extracted/2018_to_now_quaterly/' + file, 'data/extracted/2018_to_now_quaterly_shifted/' + file)

    if differ:
        remove_rolling_sum('data/extracted/2018_to_now_monthly/' + file,
                           'data/extracted/2018_to_now_monthly_differenced/' + file, 2)
        make_quarterly('data/extracted/2018_to_now_monthly_differenced/' + file, 'data/extracted/2018_to_now_quaterly/' + file)
        add_one_day_to_dates('data/extracted/2018_to_now_quaterly/' + file,
                             'data/extracted/2018_to_now_quaterly_shifted/' + file)


        remove_rolling_sum('data/extracted/2009_to_2017_quaterly/' + file,
                           'data/extracted/2009_to_2017_quaterly_diff/' + file, 4)

        combine_csvs('data/extracted/2009_to_2017_quaterly_diff/' + file,'data/extracted/2018_to_now_quaterly_shifted/' + file, 'data/extracted/complete/' + file)
    else:
        combine_csvs('data/extracted/2009_to_2017_quaterly/' + file,
                     'data/extracted/2018_to_now_quaterly_shifted/' + file, 'data/extracted/complete/' + file)


def split_csv_at_time(file_path, split_time, time_column, output_file1, output_file2):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Convert the time column to datetime format
    df[time_column] = pd.to_datetime(df[time_column])

    # Split the dataframe into two based on the specified time
    df1 = df[df[time_column] <= split_time]
    df2 = df[df[time_column] > split_time]

    # Save the split dataframes to two new CSV files
    df1.to_csv(output_file1, index=False)
    df2.to_csv(output_file2, index=False)

    return output_file1, output_file2


def combine_csvs(file1, file2, output_file):
    # Read the two CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Concatenate the two dataframes
    combined_df = pd.concat([df1, df2])

    # Sort the combined dataframe by time column if necessary (optional)
    # combined_df = combined_df.sort_values(by='timestamp')

    # Save the combined dataframe to a new CSV file
    combined_df.to_csv(output_file, index=False)

    return output_file

def make_quarterly(csv_in, csv_out, sum):
    df = pd.read_csv(csv_in)
    df = df.rename(columns={df.columns[0]: 'Date'})
    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')

    # Convert relevant columns to numeric, invalid parsing will be set as NaN
    df = df.apply(pd.to_numeric, errors='coerce')

    if sum:
        df_quarterly = df.resample('QE').sum()
    else:
        df_quarterly = df.resample('QE').mean()

    df_quarterly.index = pd.to_datetime(df_quarterly.index, format='%Y-%m-%d')
    df_quarterly.to_csv(csv_out)


def remove_rolling_sum(file_path, out_path, month):
    df = pd.read_csv(file_path, index_col=0)

    # Save the original column order
    original_columns = df.columns

    # Select only numeric columns
    numeric_df = df.select_dtypes(include='number')

    # Calculate the difference
    df_diff = numeric_df.diff(axis=0)

    # Handle the February case
    for idx in df.index:
        if datetime.strptime(idx, '%Y-%m-%d').month == month:
            df_diff.loc[idx] = numeric_df.loc[idx]

    # Combine the difference DataFrame with the original non-numeric columns
    df_diff = df_diff.combine_first(df)

    # Reorder columns to match the original order
    df_diff = df_diff[original_columns]

    # Save the result
    df_diff.to_csv(out_path)


def add_one_day_to_dates(csv_path, output_path, num=1, minus=False):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    if minus:
        # Add one day to each date
        df['Date'] = df['Date'] - timedelta(days=num)
    else:
        df['Date'] = df['Date'] + timedelta(days=num)

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_path, index=False)

def multiply_data_by_negative_one(file_path, num=-1):
    # Read the CSV file
    df = pd.read_csv(file_path)
    output_path = file_path

    # Apply the multiplication by -1 to all numeric values
    df = df.map(lambda x: x * num if isinstance(x, (int, float)) else x)

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_path, index=False)


def divide_csv_values(file1: str, file2: str, output_file: str, date_column='Date'):
    # Load the CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Ensure the date column exists in both DataFrames
    if date_column not in df1.columns or date_column not in df2.columns:
        raise ValueError(f"Date column '{date_column}' not found in one of the CSV files.")

    # Set the date column as the index for both DataFrames
    df1.set_index(date_column, inplace=True)
    df2.set_index(date_column, inplace=True)

    # Find common columns and rows
    common_columns = df1.columns.intersection(df2.columns)
    common_rows = df1.index.intersection(df2.index)

    # Filter the DataFrames to only include common columns and rows
    df1_common = df1.loc[common_rows, common_columns]
    df2_common = df2.loc[common_rows, common_columns]

    # Convert columns to numeric types
    df1_common = df1_common.apply(pd.to_numeric, errors='coerce')
    df2_common = df2_common.apply(pd.to_numeric, errors='coerce')

    # Perform element-wise division, handling division by zero and NaN values
    result_df = df1_common.copy()
    result_df = result_df.div(df2_common.replace(0, pd.NA))

    # Reset the index to include the date column in the output
    result_df.reset_index(inplace=True)

    # Save the resulting DataFrame to a new CSV file
    result_df.to_csv(output_file, index=False)


def remove_rolling_sum_effect(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Ensure the 'Date' column is datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Set the 'Date' column as the index
    df.set_index('Date', inplace=True)

    # Convert the data to numeric, forcing errors to NaN
    df = df.apply(pd.to_numeric, errors='coerce')

    # Create a copy of the dataframe to store the corrected values
    df_corrected = df.copy()

    # Iterate through the dataframe by year
    for year in df.index.year.unique():
        # Filter the data for the specific year
        df_year = df[df.index.year == year]

        # Get the months for the year
        months = df_year.index.month

        # Calculate the difference for all months except the 4th month
        for i in range(1, len(months)):
            if months[i] != 4:
                df_corrected.iloc[df.index.get_loc(df_year.index[i])] = df_year.iloc[i] - df_year.iloc[i - 1]

    return df_corrected


def extract_row_by_date(csv_file, date):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Ensure the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert the input date to a datetime object
    date = pd.to_datetime(date)

    # Find the row corresponding to the input date
    row = df[df['Date'] == date]

    # Convert the row to a list
    if not row.empty:
        return row.iloc[0].tolist()  # Extract the first row and convert to list
    else:
        print('No such row')
        return None

def update_row_by_date(csv_file, date, new_row_values):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Ensure the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Find the index of the row corresponding to the input date
    index = df[df['Date'] == date].index

    if not index.empty:
        # Update the row with the new values
        df.iloc[index[0]] = new_row_values

        # Save the updated DataFrame back to the CSV file
        df.to_csv(csv_file, index=False)
        return True
    else:
        return False


def process_bank_assets(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file, index_col='Date')

    # Convert all columns to numeric, replacing non-numeric values with NaN
    df = df.apply(pd.to_numeric, errors='coerce')

    # Calculate the total assets for each period, ignoring NaN values
    total_assets = df.sum(axis=1, skipna=True)

    # Calculate the share of each bank's assets to the total
    df = df.div(total_assets, axis=0)

    # Replace NaN with empty string for CSV output
    df = df.fillna('')

    # Save the processed data to a new CSV file
    df.to_csv(output_file)

    print(f"Processed data saved to {output_file}")


def multiply_elements_except_first(lst):
    # Multiply only negative numeric elements by -1
    result = []
    for x in lst:
        if isinstance(x, (int, float)) and x < 0:
            result.append(-x)
        else:
            result.append(x)
    return result


def apply_operation(correction, *lists):
    # Ensure correction and lists are all valid lists
    if not lists or not all(isinstance(lst, list) for lst in lists):
        raise ValueError("All inputs must be lists")

    # Ensure all lists are of the same length
    list_lengths = {len(lst) for lst in lists}
    if len(list_lengths) > 1:
        raise ValueError("All lists must be of the same length")

    # Subtract corresponding elements of the lists from correction, excluding the first element
    result = correction[:]
    for i in range(len(result)):
        if i > 0:  # Skip the first element
            for lst in lists:
                result[i] -= lst[i]

    return result

def split_connect(file, differ = False, expenses=False, Finresults=False):
    path = 'data/extracted/mixed/'
    split_csv_at_time(path + file, '2018-01-01', 'Date','data/extracted/2009_to_2017_quaterly/' + file, 'data/extracted/2018_to_now_monthly/' + file)

    if expenses:
        multiply_data_by_negative_one('data/extracted/2009_to_2017_quaterly/' + file)
        splitdate = extract_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2018-01-01')
        print(splitdate)
        splitdate = multiply_elements_except_first(splitdate)
        print(splitdate)
        update_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2018-01-01', splitdate)
    if differ:
        remove_rolling_sum('data/extracted/2018_to_now_monthly/' + file,
                           'data/extracted/2018_to_now_monthly_differenced/' + file, 2)
        if sum:
            make_quarterly('data/extracted/2018_to_now_monthly_differenced/' + file, 'data/extracted/2018_to_now_quaterly/' + file, sum=Finresults)
        add_one_day_to_dates('data/extracted/2018_to_now_quaterly/' + file,
                             'data/extracted/2018_to_now_quaterly_shifted/' + file)
        fix2018 = True
        if fix2018:
            splitdate = multiply_elements_except_first(extract_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2018-01-01'))
            #
            twenty1704 = multiply_elements_except_first(extract_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2017-04-01'))
            twenty1707 = multiply_elements_except_first(extract_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2017-07-01'))
            twenty1710 = multiply_elements_except_first(extract_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2017-10-01'))
            #
            print(splitdate)
            splitdate = apply_operation(splitdate, twenty1710)
            print(splitdate)

            adjusting = multiply_elements(extract_row_by_date('data/extracted/2018_to_now_quaterly_shifted/' + file, '2018-04-01'), 0.5*3)
            update_row_by_date('data/extracted/2018_to_now_quaterly_shifted/' + file, '2018-04-01', adjusting)
        remove_rolling_sum('data/extracted/2009_to_2017_quaterly/' + file,
                           'data/extracted/2009_to_2017_quaterly_diff/' + file, 4)
        update_row_by_date('data/extracted/2009_to_2017_quaterly_diff/' + file, '2018-01-01', splitdate)

        combine_csvs('data/extracted/2009_to_2017_quaterly_diff/' + file,'data/extracted/2018_to_now_quaterly_shifted/' + file, 'data/extracted/complete/' + file)
    else:
        if sum:
            make_quarterly('data/extracted/2018_to_now_monthly/' + file,
                       'data/extracted/2018_to_now_quaterly/' + file, sum=Finresults)
        add_one_day_to_dates('data/extracted/2018_to_now_quaterly/' + file,
                             'data/extracted/2018_to_now_quaterly_shifted/' + file)
        combine_csvs('data/extracted/2009_to_2017_quaterly/' + file,
                     'data/extracted/2018_to_now_quaterly_shifted/' + file, 'data/extracted/complete/' + file)

def multiply_elements(lst, multiplier):
    # Multiply all elements except the first one by the given multiplier
    return [lst[0]] + [x * multiplier for x in lst[1:]]

def split_connect_v2(file, differ = False, expenses=False, Finresults=False, fix2018=False):
    path = 'data/extracted/mixed/'
    split_csv_at_time(path + file, '2018-01-01', 'Date',
                      'data/extracted/2009_to_2017_quaterly/' + file,
                      'data/extracted/2018_to_now_monthly/' + file)
    add_one_day_to_dates('data/extracted/2018_to_now_monthly/' + file,
                         'data/extracted/2018_to_now_monthly_shift/' + file, 1, minus = True)
    if expenses:
        splitdate = extract_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2018-01-01')
        multiply_data_by_negative_one('data/extracted/2009_to_2017_quaterly/' + file)
        update_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2018-01-01', splitdate)

    if differ:
        remove_rolling_sum('data/extracted/2018_to_now_monthly/' + file,
                           'data/extracted/2018_to_now_monthly_differenced/' + file, 2)

        splitdate = extract_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2018-01-01')
        splitdate = multiply_elements_except_first(splitdate)
        twenty1710 = extract_row_by_date('data/extracted/2009_to_2017_quaterly/' + file, '2017-10-01')
        twenty1710 = multiply_elements_except_first(twenty1710)
        remove_rolling_sum('data/extracted/2009_to_2017_quaterly/' + file,
                           'data/extracted/2009_to_2017_quaterly_diff/' + file, 4)
        splitdate = apply_operation(splitdate, twenty1710)
        update_row_by_date('data/extracted/2009_to_2017_quaterly_diff/' + file, '2018-01-01', splitdate)


        make_quarterly('data/extracted/2018_to_now_monthly_differenced/' + file,
                   'data/extracted/2018_to_now_quaterly/' + file, sum=Finresults)

        add_one_day_to_dates('data/extracted/2018_to_now_quaterly/' + file,
                             'data/extracted/2018_to_now_quaterly_shifted/' + file, 1)

        combine_csvs('data/extracted/2009_to_2017_quaterly_diff/' + file,
                     'data/extracted/2018_to_now_quaterly_shifted/' + file, 'data/extracted/with_zeros/' + file)
    else:
        make_quarterly('data/extracted/2018_to_now_monthly/' + file,
                   'data/extracted/2018_to_now_quaterly/' + file, sum=Finresults)

        add_one_day_to_dates('data/extracted/2018_to_now_quaterly/' + file,
                             'data/extracted/2018_to_now_quaterly_shifted/' + file, 1)

        combine_csvs('data/extracted/2009_to_2017_quaterly/' + file,
                     'data/extracted/2018_to_now_quaterly_shifted/' + file, 'data/extracted/with_zeros/' + file)

    remove_zeros('data/extracted/with_zeros/' + file, 'data/extracted/complete/' + file)
    if fix2018:
        fix = extract_row_by_date('data/extracted/complete/' + file, '2018-04-01')
        fixed = multiply_except_first_for2018(fix, 3/2)
        update_row_by_date('data/extracted/complete/' + file, '2018-04-01', fixed)
    print(f"Processed {file} data saved")

def multiply_except_first_for2018(lst, multiplier):
    if len(lst) < 2:
        return lst  # Return list as-is if it has less than 2 elements
    return [lst[0]] + [x * multiplier for x in lst[1:]]
def remove_zeros(path_in, path_out):
    df = pd.read_csv(path_in)

    df.replace(0, np.nan, inplace=True)
    df.replace(0.0, np.nan, inplace=True)

    df.to_csv(path_out, index=False)


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


def calculate_net_income(income_csv_path, expense_csv_path, output_csv_path):
    # Read the income and expense CSV files
    income_df = pd.read_csv(income_csv_path)
    expense_df = pd.read_csv(expense_csv_path)

    # logger.info(f"Income DataFrame shape: {income_df.shape}")
    # logger.info(f"Expense DataFrame shape: {expense_df.shape}")

    # Ensure both dataframes have the same structure
    assert income_df.columns.equals(expense_df.columns), "Income and expense CSV files have different structures"

    # Identify numeric columns (excluding 'Date')
    numeric_columns = income_df.columns.drop('Date')

    # Function to convert to numeric, replacing non-convertible values with 0
    def safe_numeric(x):
        return pd.to_numeric(x, errors='coerce').fillna(0)

    # Apply safe conversion to numeric columns
    for df in [income_df, expense_df]:
        df[numeric_columns] = df[numeric_columns].apply(safe_numeric)

    # logger.info("Data types after conversion:")
    # logger.info(income_df.dtypes)

    # Calculate net income (income - expense)
    net_income_df = income_df.set_index('Date').subtract(expense_df.set_index('Date'))

    # Reset the index to make 'Date' a column again
    net_income_df.reset_index(inplace=True)

    # logger.info(f"Net income DataFrame shape: {net_income_df.shape}")
    # logger.info(f"Number of non-null values: {net_income_df.notnull().sum().sum()}")

    # Replace any infinite values with NaN
    net_income_df = net_income_df.replace([np.inf, -np.inf], np.nan)

    # Save the net income data to a new CSV file
    net_income_df.to_csv(output_csv_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
    #
    # logger.info(f"Net income data has been saved to {output_csv_path}")
    #
    # # Print first few rows of the net income DataFrame
    # logger.info("First few rows of net income DataFrame:")
    # logger.info(net_income_df.head().to_string())


def calculate_net_income_v2(income_csv_path, expense_csv_path, output_csv_path):
    # Read the income and expense CSV files
    income_df = pd.read_csv(income_csv_path, index_col='Date')
    expense_df = pd.read_csv(expense_csv_path, index_col='Date')

    # Calculate net income
    net_income_df = income_df - expense_df

    # Save the net income DataFrame to a new CSV file
    net_income_df.to_csv(output_csv_path)

def rainbow_print(text):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    rainbow_text = ""
    color_index = 0
    for char in text:
        if char.isspace():
            rainbow_text += char
        else:
            color = colors[color_index % len(colors)]
            rainbow_text += f"{Style.BRIGHT}{color}{char}{Style.RESET_ALL}"
            color_index += 1
    print(rainbow_text)

def get_IR(interbank=True):
    df = pd.read_excel('data/original/Міжбанк та ключова процентна ставка.xlsx')
    new_df = pd.DataFrame()
    new_df['Date'] = df['Date']
    if interbank:
        new_df['IR'] = df['Interbank IR']
        new_df.to_csv('data/extracted/Interbank.csv', index=False)
    else:
        new_df['IR'] = df['Policy IR']
        new_df.to_csv('data/extracted/Policy.csv', index=False)

@contextmanager
def suppress_output():
    # Redirects the standard output to null
    with open(os.devnull, 'w') as fnull:
        old_stdout = sys.stdout
        sys.stdout = fnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def create_median_file(input_csv_path, output_csv_path, name, statistic='median'):
    # Read the CSV file
    df = pd.read_csv(input_csv_path)

    # Check if the first column is 'Date' and set it as index
    if 'Date' in df.columns:
        df.set_index('Date', inplace=True)

    # Convert all columns to numeric, forcing errors to NaN
    df = df.apply(pd.to_numeric, errors='coerce')

    # Calculate the specified statistic for each row
    if statistic == 'median':
        result = df.median(axis=1)
    elif statistic == 'mean':
        result = df.mean(axis=1)
    else:
        raise ValueError("Statistic must be 'median' or 'mean'")

    # Create a new DataFrame with the results
    result_df = pd.DataFrame({statistic: result})
    if statistic == 'median':
        result_df = result_df.rename(columns={'median': name})
    elif statistic == 'mean':
        result_df = result_df.rename(columns={'mean': name})

    # Save the result to a new CSV file with dates in the first column
    result_df.to_csv(output_csv_path, index=True)


def combine_csvs_row_by_row(*input_files, output_file):
    # Initialize an empty DataFrame to store the merged result
    combined_df = None

    # Read and merge each input CSV file
    for file in input_files:
        df = pd.read_csv(file)

        if combined_df is None:
            combined_df = df
        else:
            # Merge the new DataFrame with the existing one, using 'outer' join on 'Date'
            combined_df = pd.merge(combined_df, df, on='Date', how='outer')

    # Sort the combined DataFrame by the 'Date' column
    combined_df.sort_values(by='Date', inplace=True)

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv(output_file, index=False)


def combine_bank_metrics(file_paths: List[Union[str, Tuple[str, str]]], common_metrics: List[str],
                         output_path: str) -> None:
    """
    Combine multiple CSV files containing bank metrics into a single CSV file.

    Args:
    file_paths (List[Union[str, Tuple[str, str]]]): List of paths to the input CSV files.
                                                    Each item can be either a string (file path) or
                                                    a tuple (file path, metric name).
    common_metrics (List[str]): List of metric names that are common to all banks.
    output_path (str): Path where the output CSV file will be saved.

    Returns:
    None
    """
    # Initialize lists to store DataFrames
    bank_specific_dfs = []
    common_dfs = {}

    # Process each input file
    for file_item in file_paths:
        if isinstance(file_item, tuple):
            file_path, metric_name = file_item
        else:
            file_path = file_item
            metric_name = os.path.splitext(os.path.basename(file_path))[0]

        # Read the CSV file
        df = pd.read_csv(file_path)

        if metric_name in common_metrics:
            # For common metrics, store the DataFrame as is
            common_dfs[metric_name] = df
        else:
            # For bank-specific metrics, melt the DataFrame
            df_melted = df.melt(id_vars=['Date'], var_name='Bank', value_name=metric_name)
            bank_specific_dfs.append(df_melted)

    # Merge all bank-specific DataFrames
    if bank_specific_dfs:
        combined_df = bank_specific_dfs[0]
        for df in bank_specific_dfs[1:]:
            combined_df = pd.merge(combined_df, df, on=['Date', 'Bank'], how='outer')
    else:
        combined_df = pd.DataFrame(columns=['Date', 'Bank'])

    # Add common metrics to the combined DataFrame
    for metric_name, df in common_dfs.items():
        # Create a temporary DataFrame with the common metric for all banks
        temp_df = combined_df[['Date', 'Bank']].merge(df, on='Date', how='left')
        temp_df = temp_df.rename(columns={temp_df.columns[-1]: metric_name})

        # Merge this temporary DataFrame with the combined DataFrame
        combined_df = pd.merge(combined_df, temp_df[['Date', 'Bank', metric_name]], on=['Date', 'Bank'], how='left')

    # Sort the DataFrame by Date and Bank
    combined_df = combined_df.sort_values(['Date', 'Bank'])

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(output_path, index=False)
    print(f"Combined data saved to {output_path}")

def sum_csv_files(file1_path, file2_path, output_path):
    # Read the CSV files
    df1 = pd.read_csv(file1_path, index_col='Date')
    df2 = pd.read_csv(file2_path, index_col='Date')

    # Get the original column order
    original_columns = df1.columns.tolist()

    # Ensure both dataframes have the same columns
    all_columns = df1.columns.union(df2.columns)
    df1 = df1.reindex(columns=all_columns, fill_value=0)
    df2 = df2.reindex(columns=all_columns, fill_value=0)

    # Function to convert to numeric, replacing non-numeric values with 0
    def to_numeric(x):
        return pd.to_numeric(x, errors='coerce').fillna(0)

    # Apply the conversion to both dataframes
    df1 = df1.apply(to_numeric)
    df2 = df2.apply(to_numeric)

    # Sum the dataframes
    result_df = df1.add(df2, fill_value=0)

    # Reorder columns to match the original order, adding any new columns at the end
    new_columns = [col for col in original_columns if col in result_df.columns]
    new_columns += [col for col in result_df.columns if col not in original_columns]
    result_df = result_df[new_columns]

    # Write the result to a new CSV file
    result_df.to_csv(output_path)

    print(f"Summed CSV file has been created at: {output_path}")

def read_bank_names(file_path):
    bank_names = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Ensure the row is not empty
                bank_names.append(row[0])  # Assuming each row has a single column
    return bank_names

def filter_banks(csv_file, banks_list_path, output_file, keep=True):
    banks_list = read_bank_names(banks_list_path)

    df = pd.read_csv(csv_file)

    if keep:
        filtered_df = df[df['Bank'].isin(banks_list)]
    else:
        filtered_df = df[~df['Bank'].isin(banks_list)]

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_file, index=False)
    print(f"Filtered data saved to {output_file}")