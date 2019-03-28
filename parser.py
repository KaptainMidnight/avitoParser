import requests
from bs4 import BeautifulSoup as bs
import csv


class Bot:
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }

    def __init__(self):
        self.get_html()

    def get_html(self):
        url = "https://m.avito.ru/rossiya/nedvizhimost"
        with requests.Session() as session:
            response = session.get(url, headers=self.headers)
        return response.text

    def parse_html(self, html):
        urls = []
        user_database = []
        soup = bs(html, 'lxml')
        main__div = soup.find_all('div', {'class': '_328WR'})
        for data in main__div:
            try:
                a = data.find('a', {'class': 'MBUbs'})['href']
                links = {
                    'href': f'https://m.avito.ru{a}'
                }
                urls.append(links)
            except:
                continue
        for user in urls:
            r = requests.get(user['href'], headers=self.headers)
            soup = bs(r.text, 'lxml')
            try:
                name = soup.find('span', {'class': 'ZvfUX'}).text
                phone = soup.find('a', {'class': '_2MOUQ'})['href']
                href = user['href']
                phone = phone[4::1]
                user_data = {
                    'name': name,
                    'phone': phone,
                    'href': href
                }
                user_database.append(user_data)
            except:
                continue
        return user_database

    def save_csv(self, data):
        with open('data.csv', 'w') as file:
            wrtr = csv.writer(file)
            wrtr.writerow(("Имя", "Номер", "Ссылка"))
            for i in data:
                wrtr.writerow((i['name'], i['phone'], i['href']))


def main():
    bot = Bot()
    html = bot.get_html()
    result = bot.parse_html(html)
    print(result)
    bot.save_csv(result)
    print("OK")


if __name__ == '__main__':
    main()
