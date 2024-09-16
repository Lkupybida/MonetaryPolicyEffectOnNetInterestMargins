from data_extraction import *
from get_data import *

if __name__ == "__main__":
    # find_all_excel_paths()
    # extract_unique_banks('data/original/Aggregation')
    # print(rename_bank('А - БАНК'))

    # Sheet name options
    # Assets   Liabilities    Capital   Finresults

    # extract_data_to_relative_vars()

    # create_composite_dataset()
    # create_composite_dataset(mean=True)
    variables = [('data/relative/admin_expenses_to_total_assets.csv', 'AE'),
                 ('data/relative/capital_to_total_assets.csv', 'LEV'),
                 ('data/relative/cash_to_total_assets.csv', 'CASH'),
                 ('data/relative/net_commision_income_to_total_assets.csv', 'NCI'),
                 ('data/relative/net_interest_income_to_total_assets.csv', 'NII'),
                 ('data/relative/total_assets.csv', 'TA'),
                 ('data/relative/securities_to_total_assets.csv', 'SEC'),
                 ('data/relative/refinanced_by_nbu_to_total_assets.csv', 'LAS'),
                 ('data/relative/Interbank.csv', 'IR'),
                 ('data/relative/Interbank_lag/Interbank_lag1.csv', 'IR_lag1'),
                 ('data/relative/Interbank_lag/Interbank_lag2.csv', 'IR_lag2'),
                 ('data/relative/Interbank_lag/Interbank_lag3.csv', 'IR_lag3'),
                 ('data/relative/Interbank_lag/Interbank_lag4.csv', 'IR_lag4'),
                 ('data/relative/Interbank_lag/Interbank_lag5.csv', 'IR_lag5'),
                 ('data/relative/Interbank_lag/Interbank_lag6.csv', 'IR_lag6'),
                 ('data/relative/Interbank_lag/Interbank_lag7.csv', 'IR_lag7'),
                 ('data/relative/ovdp_to_total_assets.csv', 'OVDP')]

    # ,
    #                  ('data/relative/Interbank_diff/Interbank_diff.csv', 'IR_diff'),
    #                  ('data/relative/Interbank_diff/Interbank_diff_lag1.csv', 'IR_diff_lag1'),
    #                  ('data/relative/Interbank_diff/Interbank_diff_lag2.csv', 'IR_diff_lag2'),
    #                  ('data/relative/Interbank_diff/Interbank_diff_lag3.csv', 'IR_diff_lag3'),
    #                  ('data/relative/Interbank_diff/Interbank_diff_lag4.csv', 'IR_diff_lag4'),
    #                  ('data/relative/Interbank_diff/Interbank_diff_lag5.csv', 'IR_diff_lag5'),
    #                  ('data/relative/Interbank_diff/Interbank_diff_lag6.csv', 'IR_diff_lag6'),
    #                  ('data/relative/Interbank_diff/Interbank_diff_lag7.csv', 'IR_diff_lag7')

    # ,
    #                       'IR_diff', 'IR_diff_lag1', 'IR_diff_lag2', 'IR_diff_lag3',
    #                       'IR_diff_lag4', 'IR_diff_lag5', 'IR_diff_lag6', 'IR_diff_lag7'

    common_metrics = ['IR', 'IR_lag1', 'IR_lag2', 'IR_lag3',
                      'IR_lag4', 'IR_lag5', 'IR_lag6', 'IR_lag7']

    # combine_bank_metrics(variables, common_metrics, 'data/for_regressing/flattened.csv')



    # filter_banks('data/for_regressing/flattened.csv',
    #              'data/for_regressing/banks_groups/functioning_or_not/functioning_banks_list.csv',
    #              'data/for_regressing/banks_groups/functioning_or_not/functioning.csv')
    # filter_banks('data/for_regressing/flattened.csv',
    #              'data/for_regressing/banks_groups/functioning_or_not/functioning_banks_list.csv',
    #              'data/for_regressing/banks_groups/functioning_or_not/not_functioning.csv',
    #              keep=False)
    #
    # filter_banks('data/for_regressing/flattened.csv',
    #              'data/for_regressing/banks_groups/top25_or_not/top25_banks_list.csv',
    #              'data/for_regressing/banks_groups/top25_or_not/top25.csv')
    # filter_banks('data/for_regressing/flattened.csv',
    #              'data/for_regressing/banks_groups/top25_or_not/top25_banks_list.csv',
    #              'data/for_regressing/banks_groups/top25_or_not/rest.csv',
    #              keep=False)

    # filter_banks('data/for_regressing/flattened.csv',
    #              'data/for_regressing/banks_groups/gov_or_private/gov_list.csv',
    #              'data/for_regressing/banks_groups/gov_or_private/gov.csv')
    # filter_banks('data/for_regressing/flattened.csv',
    #              'data/for_regressing/banks_groups/gov_or_private/gov_list.csv',
    #              'data/for_regressing/banks_groups/gov_or_private/private.csv',
    #              keep=False)

    # create_median_file('data/extracted/complete/net_interest_income.csv',
    #                        'data/relative/averaged/NII_averaged_not_relative.csv', 'NII',
    #                        statistic = 'median')

    # create_median_file('data/extracted/2018_to_now_monthly/refinanced_by_nbu.csv',
    #                    'data/relative/averaged/refinanced.csv', 'LAS',
    #                    statistic='median')
    # create_median_file('data/extracted/2018_to_now_monthly/securities.csv',
    #                    'data/relative/averaged/securities_mean.csv', 'SEC',
    #                    statistic = 'mean')

    # combine_csvs_row_by_row('data/relative/averaged/securities2.csv',
    #                         'data/relative/averaged/refinanced.csv',
    #                         output_file='data/relative/averaged/securities_and_refinanced.csv')

    # filter_banks('data/for_regressing/flattened.csv',
    #              'data/for_regressing/banks_groups/top10_or_not/top10_banks_list.csv',
    #              'data/for_regressing/banks_groups/top10_or_not/top10.csv')
    # filter_banks('data/for_regressing/flattened.csv',
    #              'data/for_regressing/banks_groups/top10_or_not/top10_banks_list.csv',
    #              'data/for_regressing/banks_groups/top10_or_not/rest.csv',
    #              keep=False)

    filter_banks('../data/for_regressing/flattened.csv',
                 'data/for_regressing/banks_groups/top10nongov_or_not/top10_banks_list.csv',
                 'data/for_regressing/banks_groups/top10nongov_or_not/top10.csv')
    filter_banks('../data/for_regressing/flattened.csv',
                 'data/for_regressing/banks_groups/top10nongov_or_not/top10_banks_list.csv',
                 'data/for_regressing/banks_groups/top10nongov_or_not/rest.csv',
                 keep=False)

    filter_banks('../data/for_regressing/flattened.csv',
                 'data/for_regressing/banks_groups/top5nongov_or_not/top5_banks_list.csv',
                 'data/for_regressing/banks_groups/top5nongov_or_not/top5.csv')
    filter_banks('../data/for_regressing/flattened.csv',
                 'data/for_regressing/banks_groups/top5nongov_or_not/top5_banks_list.csv',
                 'data/for_regressing/banks_groups/top5nongov_or_not/rest.csv',
                 keep=False)