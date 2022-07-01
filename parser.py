from bs4 import BeautifulSoup
import requests
import sys


def parse_towns_table():
    # hardcoded as we have only one page
    url = 'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B8%D0%B5_%D0%BD%D0%B0%D1%81%D0' \
          '%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B5_%D0%BF%D1%83%D0%BD%D0%BA%D1%82%D1%8B_%D0%9C%D0%BE%D1%81%D0%BA%D0' \
          '%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B9_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D0%B8 '
    page = requests.get(url)
    if page.status_code == 200:
        towns_list = []
        soup = BeautifulSoup(page.text, "html.parser")
        first_table_rows = soup.find_all('table', class_='standard')[0].find('tbody').find_all('tr')[1:]
        # print(first_table_rows)
        for row in first_table_rows:
            town_info = []
            cols = row.findAll('td')
            # town id
            town_info.append(cols[0].text.strip())
            # town name
            town_info.append(cols[1].text.strip())
            # town district
            town_info.append(cols[2].text.strip())
            # town population
            town_info.append(int(cols[4]['data-sort-value'].strip()))
            # town wiki link
            town_info.append('https://ru.wikipedia.org' + cols[1].a['href'])
            towns_list.append(town_info)
        return towns_list
    else:
        print(f'Code: {page.status_code}', file=sys.stderr)
