from data_extraction import *

total_assets = ["Усього активів", "Усього активів", "Загальні активи, усього"]
admin_expenses = ['Адміністративні та інші операційні витрати',
                  'Адміністративні та інші операційні витрати',
                  'Адміністра-тивні та інші операційні витрати']
net_interest_income = ['Чистий процентний дохід/(Чисті процентні витрати)',
                       'Чистий процентний дохід/ (Чисті процентні витрати)',
                       'Чистий процентний дохід/(Чисті процентні витрати)',
                       'Чистий процентний дохід']

bonds = ['Довідково: ОВДП', 'ОВДП']

commision = ['Чистий комісійний дохід/(Чисті комісійні витрати)',
             'Чистий комісійний дохід/ (Чисті комісійні витрати)',
             'Чистий комісійний дохід']

commision_income = ['Комісійні доходи',
                    'Комісійні доходи',
                    'Комісійні доходи']

commision_expenses = ['Комісійні витрати',
                      'Комісійні витрати',
                      'Комісійні витрати ',
                      'Комісійні витрати']

capital = ['Усього власного капіталу',
           'Усього власного капіталу',
           'Усього власного капіталу',
           'Усього власного капіталу ']

capital_to_assets = rainbow_print_save('\nTotal Capital to Total Assets calculated and saved')
ae_to_assets = rainbow_print_save('\nAdministrative Expenses to Total Assets calculated and saved')
OVDP_to_assets = rainbow_print_save('\nOVDP to Total Assets calculated and saved')
commision_to_assets = rainbow_print_save('\nNet Commision Income to Total Assets calculated and saved')
NII_to_assets = rainbow_print_save('\nNet Interest Income to Total Assets calculated and saved')
Assets_to_assets = rainbow_print_save('\nBank Assets to Total Assets calculated and saved')