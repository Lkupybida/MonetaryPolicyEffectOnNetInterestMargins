from data_extraction import *
from col_names import *

def relative_total_assets():
    extract_bank_data('Assets', total_assets, 'data/extracted/mixed/total_assets.csv')
    split_connect_v2('total_assets.csv')
    process_bank_assets('data/extracted/complete/total_assets.csv', 'data/relative/total_assets.csv')

    # rainbow_print('\nBank Assets to Total Assets calculated and saved')
    print(Assets_to_assets)

def net_interest_income_to_total_assets():
    extract_bank_data('Finresults', net_interest_income, 'data/extracted/mixed/net_interest_income.csv')
    split_connect_v2('net_interest_income.csv', differ=True, Finresults=True)
    extract_bank_data('Assets', total_assets, 'data/extracted/mixed/total_assets.csv')
    split_connect_v2('total_assets.csv')
    divide_csv_values('data/extracted/complete/net_interest_income.csv', 'data/extracted/complete/total_assets.csv',
                      'data/relative/net_interest_income_to_total_assets.csv')

    # rainbow_print('\nNet Interest Income to Total Assets calculated and saved')
    print(NII_to_assets)

def net_commision_income_to_total_assets():
    # extract_bank_data('Finresults', commision, 'data/extracted/mixed/net_commision_income.csv')

    extract_bank_data('Finresults', commision_income, 'data/extracted/mixed/commision_income.csv')
    extract_bank_data('Finresults', commision_expenses, 'data/extracted/mixed/commision_expenses.csv')
    dates = pd.date_range(start='2009-04-01', end='2017-10-01', freq='3MS').strftime('%Y-%m-%d').tolist()
    for date in dates:
        splitdate = extract_row_by_date('data/extracted/mixed/commision_expenses.csv', date)
        splitdate = multiply_elements_except_first(splitdate)
        update_row_by_date('data/extracted/mixed/commision_expenses.csv', date, splitdate)

    # minus
    calculate_net_income('data/extracted/mixed/commision_income.csv',
                         'data/extracted/mixed/commision_expenses.csv',
                         'data/extracted/mixed/net_commision_income.csv')

    split_connect_v2('net_commision_income.csv', differ=True, Finresults=True)


    extract_bank_data('Assets', total_assets, 'data/extracted/mixed/total_assets.csv')
    split_connect_v2('total_assets.csv')
    divide_csv_values('data/extracted/complete/net_commision_income.csv', 'data/extracted/complete/total_assets.csv',
                      'data/relative/net_commision_income_to_total_assets.csv')

    # rainbow_print('\nNet Commision Income to Total Assets calculated and saved')
    print(commision_to_assets)

def ovdp_to_total_assets():
    extract_bank_data('Assets', total_assets, 'data/extracted/mixed/total_assets.csv')
    split_connect_v2('total_assets.csv')
    extract_bank_data('Assets', bonds, 'data/extracted/mixed/ovdp.csv')
    split_connect_v2('ovdp.csv')
    divide_csv_values('data/extracted/complete/ovdp.csv', 'data/extracted/complete/total_assets.csv',
                      'data/relative/ovdp_to_total_assets.csv')

    # rainbow_print('\nOVDP to Total Assets calculated and saved')
    print(OVDP_to_assets)

def admin_expenses_to_total_assets():
    extract_bank_data('Finresults', admin_expenses, 'data/extracted/mixed/admin_expenses.csv')
    split_connect_v2('admin_expenses.csv', differ=True, expenses=True, Finresults=True)
    extract_bank_data('Assets', total_assets, 'data/extracted/mixed/total_assets.csv')
    split_connect_v2('total_assets.csv')
    divide_csv_values('data/extracted/complete/admin_expenses.csv', 'data/extracted/complete/total_assets.csv',
                      'data/relative/admin_expenses_to_total_assets.csv')

    # rainbow_print('\nAdministrative Expenses to Total Assets calculated and saved')
    print(ae_to_assets)

def capital_to_total_assets():
    extract_bank_data('Capital', capital, 'data/extracted/mixed/capital.csv')
    split_connect_v2('capital.csv')
    extract_bank_data('Assets', total_assets, 'data/extracted/mixed/total_assets.csv')
    split_connect_v2('total_assets.csv')

    divide_csv_values('data/extracted/complete/capital.csv', 'data/extracted/complete/total_assets.csv',
                      'data/relative/capital_to_total_assets.csv')

    # rainbow_print('\nTotal Capital to Total Assets calculated and saved')
    print(capital_to_assets)