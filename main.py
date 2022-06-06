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
    assortment = excel_data_df.to_dict('records')

    wines = defaultdict(list)
    for product in assortment:
        key = product["Категория"]
        wines[key].append(product)

    foundation_date = datetime.datetime(year=1920, month=1, day=1)
    today = datetime.date.today()
    winery_age = today.year - foundation_date.year

    if (winery_age%10 == 1) and (winery_age != 11) and (winery_age != 111):
        suffix = "год"
    elif (winery_age%10 > 1) and (winery_age%10 < 5) and (winery_age != 12) and (winery_age != 13) and (winery_age != 14):
        suffix = "года"
    else:
        suffix = "лет"

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        age = winery_age,
        wines = wines,
        suffix = suffix
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()