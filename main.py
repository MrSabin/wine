import argparse
import datetime
import os
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help = 'Путь к файлу',
        default = os.path.join(os.getcwd(), 'wines_table.xlsx'))
    args = parser.parse_args()

    excel_data_df = pandas.read_excel(args.path,
        na_values="None", 
        keep_default_na=False)
    wines_data = excel_data_df.to_dict('records')

    wines = defaultdict(list)
    for item in wines_data:
        key = item["Категория"]
        wines[key].append(item)

    foundation_date = datetime.datetime(year=1920, month=1, day=1)
    today = datetime.date.today()
    delta = today.year - foundation_date.year

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

if __name__ == '__main__':
    main()