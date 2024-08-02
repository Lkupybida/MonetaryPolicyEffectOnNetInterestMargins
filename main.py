from extraction import *

if __name__ == "__main__":
    # extract_bank_data('data/original/Aggregation', 'Фінрез', 'Чистий процентний дохід/(Чисті процентні витрати)',
    #                   'data/extracted/2018_to_now_monthly/', 'NII.csv')
    # extract_bank_data('data/original/Aggregation', 'Активи', 'Загальні активи, усього',
    #                   'data/extracted/2018_to_now_monthly/', 'TA.csv')
    # make_quarterly('data/extracted/2018_to_now_monthly/', 'NII.csv', 'data/extracted/2018_to_now_quaterly/')

    # xlsx2csv('data/original/Міжбанк та ключова процентна ставка.xlsx', 'data/extracted/PR.csv')


    # remove_rolling_sum('data/extracted/2018_to_now_monthly/NII.csv',
    #                    'data/extracted/2018_to_now_monthly_differenced/NII.csv')
    # make_quarterly('data/extracted/2018_to_now_monthly_differenced/', 'NII.csv', 'data/extracted/2018_to_now_quaterly/')
    # make_quarterly('data/extracted/2018_to_now_monthly/', 'TA.csv', 'data/extracted/2018_to_now_quaterly/')
    #
    # divide('data/extracted/2018_to_now_quaterly/NII.csv',
    #        'data/extracted/2018_to_now_quaterly/TA.csv',
    #        'data/extracted/2018_to_now_quaterly/NIM.csv')

    # extract_unique_banks('data/original/Aggregation')
    what_col_bank_data_starts(3, 8)
    ex()
