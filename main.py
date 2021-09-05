import requests
from bs4 import BeautifulSoup


class WebSpider(object):
    def __init__(self):
        self.url = 'https://www.ted.com/talks'
        self.talks = []
        self.links = []

    def get_talks_links(self):
        resp = requests.get(self.url)
        response = resp.text
        bs = BeautifulSoup(response, 'html.parser')
        browser_results_div = bs.find('div', id='browse-results')
        h4_list = browser_results_div.find_all('h4', class_='f-w:700 h9 m5')
        print(h4_list)

        lines = ''
        for item in h4_list:
            line = item.find('a').string
            href = item.find('a').get('href')
            # print(line)
            # lines += line
            self.talks.append(line)
            self.links.append(href + '\n')
            # print(item.find('a').get('h4'))

        print(self.links)
        return lines

    def write_file(self, path, text):
        with open(path, mode='w', encoding='UTF-8') as file:
            file.writelines(text)


if __name__ == '__main__':
    webSpider = WebSpider()
    text = webSpider.get_talks_links()
    webSpider.write_file('talks.txt', webSpider.talks)
    webSpider.write_file('links.txt', webSpider.links)
