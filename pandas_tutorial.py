import pandas as pd

import pprint

excel_data_df = pd.read_excel(
	"wine2.xlsx", na_values="None", 
	keep_default_na=False)
wines_list = excel_data_df.to_dict('records')

white_wines = []
red_wines = []
drinks = []

for col in wines_list:
	if "Белые вина" in col.values():
		white_wines.append(col)
	elif "Красные вина" in col.values():
		red_wines.append(col)
	else:
		drinks.append(col)

categories = ["Белые вина", "Красные вина", "Напитки"]
category_list = dict.fromkeys(categories, [])
category_list["Белые вина"] = white_wines
category_list["Красные вина"] = red_wines
category_list["Напитки"] = drinks

pp = pprint.PrettyPrinter()
pp.pprint(category_list)