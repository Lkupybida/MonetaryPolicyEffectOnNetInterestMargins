from data_extraction import *

def rainbow_print_save(text):
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
    return rainbow_text

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

cash = ['Грошові кошти та їх еквіваленти',
        'Грошові кошти та їх еквіваленти',
        'Грошові кошти та їх еквіваленти',
        'Грошові кошти та їх еквіваленти',
        'Грошові кошти та їх еквіваленти',
        'Грошові кошти та їх еквіваленти',
        'Грошові кошти та їх еквіваленти']

securities1 = ['Цінні папери в портфелі банку на продаж',
               'Цінні папери, які обліковуються за справедливою вартістю через інший сукупний дохід',
               '"Цінні папери, які обліковуються за справедливою вартістю через інший сукупний дохід"',
               'Цінні папери, які обліковуються за справедливою вартістю через інший сукупний дохід',
               'Цінні папери в портфелі банку на продаж',
               'Цінні папери в портфелі банку на продаж',
               'Цінні папери в портфелі банку на продаж',
               'Цінні папери, які обліковуються за справедливою вартістю']

securities2 = ['Цінні папери в портфелі банку до погашення',
               'Цінні папери, які обліковуються за амортизованою собівартістю',
               '"Цінні папери, які обліковуються за амортизованою собівартістю"',
               'Цінні папери в портфелі банку до погашення',
               'Цінні папери в портфелі банку до погашення',
               'Цінні папери в портфелі банку до погашення',
               'амортизованою']

capital_to_assets = rainbow_print_save('\nTotal Capital to Total Assets calculated and saved')
ae_to_assets = rainbow_print_save('\nAdministrative Expenses to Total Assets calculated and saved')
OVDP_to_assets = rainbow_print_save('\nOVDP to Total Assets calculated and saved')
commision_to_assets = rainbow_print_save('\nNet Commision Income to Total Assets calculated and saved')
NII_to_assets = rainbow_print_save('\nNet Interest Income to Total Assets calculated and saved')
Assets_to_assets = rainbow_print_save('\nBank Assets to Total Assets calculated and saved')
interbank = rainbow_print_save('\nInterbank IR calculated and saved')
policy = rainbow_print_save('\nPolicy IR calculated and saved')
Cash_to_Assets = rainbow_print_save('\nShare of Cash to Total Assets calculated and saved')
Securities = rainbow_print_save('\nShare of Securities to Total Assets calculated and saved')
LiquidAss = rainbow_print_save('\nShare of Liquid Assets to Total Assets calculated and saved')