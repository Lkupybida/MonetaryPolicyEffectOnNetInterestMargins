import pandas as pd
import matplotlib.pyplot as plt


def plot_IR(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path, index_col='Date')
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')

    # Filter data from 2018 to 2024
    start_date = '2018-01-01'
    end_date = '2024-12-31'
    mask = (df.index >= start_date) & (df.index <= end_date)
    df_filtered = df.loc[mask]

    # Create the plot
    plt.figure(figsize=(14, 8))
    # Load total_income.csv and total_assets.csv
    df_net_interest_income = pd.read_csv('data/extracted/2018_to_now_quaterly/NII.csv', index_col=0)
    df_assets = pd.read_csv('data/extracted/2018_to_now_quaterly/TA.csv', index_col=0)

    # Calculate the ratio of income to assets for each bank
    ratio_df = (df_net_interest_income.mean(axis=1) / df_assets.mean(axis=1)) * 10000

    plt.plot(pd.to_datetime(ratio_df.index), ratio_df, label='NIM')
    plt.plot(df_filtered.index, df_filtered['Interbank IR'], label='Interbank IR')
    plt.plot(df_filtered.index, df_filtered['Policy IR'], label='Policy IR')

    # Set title and labels
    plt.title('Interbank to Policy IR (2018-2024)')
    plt.xlabel('Date')
    plt.ylabel('%')
    plt.legend()
    plt.grid(True)

    # Rotate and align the tick labels so they look better
    plt.gcf().autofmt_xdate()

    # Use tight layout to prevent clipping of tick-labels
    plt.tight_layout()

def plot_aver(file_path):
    df = pd.read_csv(file_path, index_col=0)
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    df['Total'] = df.mean(axis=1)
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Total'], label='Average')

    plt.title('Average')
    plt.xlabel('Date')
    # plt.ylabel('NIM')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_total(file_path):
    df = pd.read_csv(file_path, index_col=0)
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    df['Total'] = df.sum(axis=1)
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Total'], label='Total')

    plt.title('Total')
    plt.xlabel('Date')
    # plt.ylabel('NIM')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()