import pandas

import pprint

excel_data_df = pandas.read_excel("wine2.xlsx")
wines_list = excel_data_df.to_dict('records')
print(wines_list)