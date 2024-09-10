from data_extraction import *
from col_names import *
from tqdm import tqdm

def relative_total_assets():
    total_steps = 3
    progress_bar = tqdm(total=total_steps, desc="Relative Total Assets")

    with suppress_output():
        extract_bank_data('Assets', total_assets, 'data/extracted/mixed/total_assets.csv')
        progress_bar.update(1)

        split_connect_v2('total_assets.csv')
        progress_bar.update(1)

        process_bank_assets('data/extracted/complete/total_assets.csv', 'data/relative/total_assets.csv')
        progress_bar.update(1)

    progress_bar.close()
    print(Assets_to_assets)

def net_interest_income_to_total_assets():
    total_steps = 5
    progress_bar = tqdm(total=total_steps, desc="Net Interest Income to Total Assets")

    with suppress_output():
        extract_bank_data('Finresults', net_interest_income, 'data/extracted/mixed/net_interest_income.csv')
        progress_bar.update(1)

        split_connect_v2('net_interest_income.csv', differ=True, Finresults=True)
        progress_bar.update(1)

        extract_bank_data('Assets', total_assets, 'data/extracted/mixed/total_assets.csv')
        progress_bar.update(1)

        split_connect_v2('total_assets.csv')
        progress_bar.update(1)

        divide_csv_values('data/extracted/complete/net_interest_income.csv', 'data/extracted/complete/total_assets.csv',
                          'data/relative/net_interest_income_to_total_assets.csv')
        progress_bar.update(1)

    progress_bar.close()
    print(NII_to_assets)

def net_commision_income_to_total_assets():
    total_steps = 9
    progress_bar = tqdm(total=total_steps, desc="Net Commision Income to Total Assets")

    with suppress_output():
        extract_bank_data('Finresults', commision_income, 'data/extracted/mixed/commision_income.csv')
        progress_bar.update(1)

        extract_bank_data('Finresults', commision_expenses, 'data/extracted/mixed/commision_expenses.csv')
        progress_bar.update(1)

        dates = pd.date_range(start='2009-04-01', end='2017-10-01', freq='3MS').strftime('%Y-%m-%d').tolist()
        for date in dates:
            splitdate = extract_row_by_date('data/extracted/mixed/commision_expenses.csv', date)
            splitdate = multiply_elements_except_first(splitdate)
            update_row_by_date('data/extracted/mixed/commision_expenses.csv', date, splitdate)
            progress_bar.update(1 / len(dates))

        calculate_net_income('data/extracted/mixed/commision_income.csv',
                             'data/extracted/mixed/commision_expenses.csv',
                             'data/extracted/mixed/net_commision_income.csv')
        progress_bar.update(1)

        split_connect_v2('net_commision_income.csv', differ=True, Finresults=True)
        progress_bar.update(1)

        extract_bank_data('Assets', total_assets, 'data/extracted/mixed/total_assets.csv')
        progress_bar.update(1)

        split_connect_v2('total_assets.csv')
        progress_bar.update(1)

        divide_csv_values('data/extracted/complete/net_commision_income.csv', 'data/extracted/complete/total_assets.csv',
                          'data/relative/net_commision_income_to_total_assets.csv')
        progress_bar.update(1)

    progress_bar.close()
    print(commision_to_assets)

def ovdp_to_total_assets():
    total_steps = 5
    progress_bar = tqdm(total=total_steps, desc="OVDP to Total Assets")

    with suppress_output():
        extract_bank_data('Assets', total_assets, 'data/extracted/mixed/total_assets.csv')
        progress_bar.update(1)

        split_connect_v2('total_assets.csv')
        progress_bar.update(1)

        extract_bank_data('Assets', bonds, 'data/extracted/mixed/ovdp.csv')
        progress_bar.update(1)

        split_connect_v2('ovdp.csv')
        progress_bar.update(1)

        divide_csv_values('data/extracted/complete/ovdp.csv', 'data/extracted/complete/total_assets.csv',
                          'data/relative/ovdp_to_total_assets.csv')
        progress_bar.update(1)

    progress_bar.close()
    print(OVDP_to_assets)

def admin_expenses_to_total_assets():
    total_steps = 5
    progress_bar = tqdm(total=total_steps, desc="Admin Expenses to Total Assets")

    with suppress_output():
        extract_bank_data('Finresults', admin_expenses, 'data/extracted/mixed/admin_expenses.csv')
        progress_bar.update(1)

        split_connect_v2('admin_expenses.csv', differ=True, expenses=True, Finresults=True)
        progress_bar.update(1)

        extract_bank_data('Assets', total_assets, 'data/extracted/mixed/total_assets.csv')
        progress_bar.update(1)

        split_connect_v2('total_assets.csv')
        progress_bar.update(1)

        divide_csv_values('data/extracted/complete/admin_expenses.csv', 'data/extracted/complete/total_assets.csv',
                          'data/relative/admin_expenses_to_total_assets.csv')
        progress_bar.update(1)

    progress_bar.close()
    print(ae_to_assets)

def capital_to_total_assets():
    total_steps = 4
    progress_bar = tqdm(total=total_steps, desc="Capital to Total Assets")

    with suppress_output():
        extract_bank_data('Capital', capital, 'data/extracted/mixed/capital.csv')
        progress_bar.update(1)

        split_connect_v2('capital.csv')
        progress_bar.update(1)

        extract_bank_data('Assets', total_assets, 'data/extracted/mixed/total_assets.csv')
        progress_bar.update(1)

        split_connect_v2('total_assets.csv')
        progress_bar.update(1)

        divide_csv_values('data/extracted/complete/capital.csv', 'data/extracted/complete/total_assets.csv',
                          'data/relative/capital_to_total_assets.csv')
        progress_bar.update(1)

    progress_bar.close()
    print(capital_to_assets)

def InterbankIR():
    total_steps = 3
    progress_bar = tqdm(total=total_steps, desc="Interbank IR")

    get_IR()
    progress_bar.update(1)

    make_quarterly('data/extracted/Interbank.csv', 'data/extracted/Interbank.csv', False)
    progress_bar.update(1)

    add_one_day_to_dates('data/extracted/Interbank.csv',
                         'data/relative/Interbank.csv', 1)
    progress_bar.update(1)

    progress_bar.close()
    print(interbank)

def PolicyIR():
    total_steps = 3
    progress_bar = tqdm(total=total_steps, desc="Policy IR")

    get_IR(interbank=False)
    progress_bar.update(1)

    make_quarterly('data/extracted/Policy.csv', 'data/extracted/Policy.csv', False)
    progress_bar.update(1)

    add_one_day_to_dates('data/extracted/Policy.csv',
                         'data/relative/Policy.csv', 1)
    progress_bar.update(1)

    progress_bar.close()
    print(policy)

def share_of_cash():
    total_steps = 3
    progress_bar = tqdm(total=total_steps, desc="Relative Share of Cash Assets")

    with suppress_output():
        extract_bank_data('Assets', cash, 'data/extracted/mixed/cash.csv')
        progress_bar.update(1)

        split_connect_v2('cash.csv')
        progress_bar.update(1)

        divide_csv_values('data/extracted/complete/cash.csv', 'data/extracted/complete/total_assets.csv',
                          'data/relative/cash_to_total_assets.csv')
        progress_bar.update(1)

        progress_bar.close()
    print(Cash_to_Assets)

def share_of_securities():
    total_steps = 5
    progress_bar = tqdm(total=total_steps, desc="Relative Securities")

    with suppress_output():
        # extract_bank_data('Assets', securities1, 'data/extracted/mixed/securities/securities1.csv')
        progress_bar.update(1)
        # extract_bank_data('Assets', securities2, 'data/extracted/mixed/securities/securities2.csv')
        progress_bar.update(1)

        sum_csv_files('data/extracted/mixed/securities/securities1.csv', 'data/extracted/mixed/securities/securities2.csv', 'data/extracted/mixed/securities.csv')
        progress_bar.update(1)

        split_connect_v2('securities.csv')
        progress_bar.update(1)

        divide_csv_values('data/extracted/complete/securities.csv', 'data/extracted/complete/total_assets.csv',
                          'data/relative/securities_to_total_assets.csv')
        progress_bar.update(1)

    progress_bar.close()
    print(Securities)

def share_of_liquid_assets():
    file = 'refinanced_by_nbu.csv'

    add_one_day_to_dates('data/extracted/2018_to_now_monthly/' + file,
                         'data/extracted/2018_to_now_monthly_shift/' + file, 1, minus=True)
    check = True
    if check:
        make_quarterly('data/extracted/2018_to_now_monthly/' + file,
                       'data/extracted/2018_to_now_quaterly/' + file, sum=False)

        add_one_day_to_dates('data/extracted/2018_to_now_quaterly/' + file,
                             'data/extracted/with_zeros/' + file, 1)


    remove_zeros('data/extracted/with_zeros/' + file, 'data/extracted/complete/' + file)
    print(f"Processed {file} data saved")
    total_steps = 5
    progress_bar = tqdm(total=total_steps, desc="Relative Liquid Assets")

    with suppress_output():

        # split_connect_v2('refinanced_by_nbu.csv')
        progress_bar.update(1)

        divide_csv_values('data/extracted/complete/refinanced_by_nbu.csv', 'data/extracted/complete/total_assets.csv',
                          'data/relative/refinanced_by_nbu_to_total_assets.csv')
        progress_bar.update(1)

    progress_bar.close()
    print(LiquidAss)

def extract_data_to_relative_vars():
    total_steps = 10
    progressss_bar = tqdm(total=total_steps, desc="Creating Dataset")
    relative_total_assets()
    progressss_bar.update(1)
    net_interest_income_to_total_assets()
    progressss_bar.update(1)
    ovdp_to_total_assets()
    progressss_bar.update(1)
    admin_expenses_to_total_assets()
    progressss_bar.update(1)
    net_commision_income_to_total_assets()
    progressss_bar.update(1)
    capital_to_total_assets()
    progressss_bar.update(1)
    InterbankIR()
    progressss_bar.update(1)
    PolicyIR()
    progressss_bar.update(1)
    share_of_cash()
    progressss_bar.update(1)
    share_of_securities()
    progressss_bar.update(1)
    suppress_output()
    rainbow_print('\nDataset completely completed')

def create_composite_dataset(mean=False):
    if mean:
        create_median_file('data/relative/net_interest_income_to_total_assets.csv',
                           'data/relative/averaged/NII_averaged.csv', 'NII',
                           statistic = 'mean')
        create_median_file('data/relative/admin_expenses_to_total_assets.csv',
                           'data/relative/averaged/AE_averaged.csv', 'AE',
                           statistic = 'mean')
        create_median_file('data/relative/net_commision_income_to_total_assets.csv',
                           'data/relative/averaged/NCI_averaged.csv', 'NCI',
                           statistic = 'mean')
        create_median_file('data/relative/capital_to_total_assets.csv',
                           'data/relative/averaged/LEV_averaged.csv', 'LEV',
                           statistic='mean')
        create_median_file('data/relative/total_assets.csv',
                           'data/relative/averaged/TA_averaged.csv', 'TA',
                           statistic='mean')
        create_median_file('data/relative/cash_to_total_assets.csv',
                           'data/relative/averaged/CASH_averaged.csv', 'CASH',
                           statistic='mean')

        combine_csvs_row_by_row('data/relative/averaged/NII_averaged.csv',
                                'data/relative/Interbank.csv',
                                'data/relative/averaged/AE_averaged.csv',
                                'data/relative/averaged/NCI_averaged.csv',
                                'data/relative/averaged/LEV_averaged.csv',
                                'data/relative/averaged/TA_averaged.csv',
                                'data/relative/median/CASH_averaged.csv',
                                output_file='data/for_regressing/averaged_dataset.csv')
    else:
        create_median_file('data/relative/net_interest_income_to_total_assets.csv',
                           'data/relative/median/NII_averaged.csv', 'NII')
        create_median_file('data/relative/admin_expenses_to_total_assets.csv',
                           'data/relative/median/AE_averaged.csv', 'AE')
        create_median_file('data/relative/net_commision_income_to_total_assets.csv',
                           'data/relative/median/NCI_averaged.csv', 'NCI')
        create_median_file('data/relative/capital_to_total_assets.csv',
                           'data/relative/median/LEV_averaged.csv', 'LEV')
        create_median_file('data/relative/total_assets.csv',
                           'data/relative/median/TA_averaged.csv', 'TA')
        create_median_file('data/relative/cash_to_total_assets.csv',
                           'data/relative/median/CASH_averaged.csv', 'CASH')

        combine_csvs_row_by_row('data/relative/median/NII_averaged.csv',
                                'data/relative/Interbank.csv',
                                'data/relative/median/AE_averaged.csv',
                                'data/relative/median/NCI_averaged.csv',
                                'data/relative/median/LEV_averaged.csv',
                                'data/relative/median/TA_averaged.csv',
                                'data/relative/median/CASH_averaged.csv',
                                output_file='data/for_regressing/median_dataset.csv')
