from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

from collections import defaultdict

import datetime

import pandas

#reading xls file to dataframe
excel_data_df = pandas.read_excel("wine3.xlsx",
    na_values="None", 
    keep_default_na=False)
wines_list = excel_data_df.to_dict('records')

#create dictonary of goods
wines = defaultdict(list)
for rec in wines_list:
    key = rec["Категория"]
    wines[key].append(rec)

begin = datetime.datetime(year=1920, month=1, day=1)
now = datetime.date.today()
delta = now.year - begin.year

if (delta%10 == 1) and (delta != 11) and (delta != 111):
   year_word = "год"
elif (delta%10 > 1) and (delta%10 < 5) and (delta != 12) and (delta != 13) and (delta != 14):
   year_word = "года"
else:
   year_word = "лет"

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    age = delta,
    wines = wines,
    word = year_word
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
#server.serve_forever()
