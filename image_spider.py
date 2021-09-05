import requests
from bs4 import BeautifulSoup
from contextlib import closing
import os, sys


class ImageSpider(object):
    def __init__(self):
        self.url = 'https://www.ted.com/talks'
        # self.url_bak = 'http://127.0.0.1:8080/ted/talks.html'
        self.talks = []
        self.links = []

    def get_images_links(self):
        resp = requests.get(self.url)
        response = resp.text
        bs = BeautifulSoup(response, 'html.parser')
        browser_results_div = bs.find('div', id='browse-results')
        # h4_list = browser_results_div.find_all('h4', class_='f-w:700 h9 m5')
        image_url_list = browser_results_div.find_all('img')
        # print(image_list)

        one_url = image_url_list[0]
        print('---- ---')
        print(len(image_url_list))
        for item in image_url_list:
            # print(item.find('img').get('src'))
            print(item.get('src'))
            self.links.append(item.get('src'))

        return self.links

    def start_download(self):
        links = self.links
        pic_dir = '/Users/shengjiesong/pic/'
        # os.mkdir(pic_dir)
        for link in links:
            img_name = link.split('/')[-1].split('?')[0]

            self.download_image(pic_dir, link, img_name)


    def download_image(self, path, image_url, filename):
        image_path = os.path.join(path, filename)
        request_headers = {'Accept': '*/*',
                           'Accept-Encoding': 'gzip, deflate, br',
                           'Accept-Language': 'zh-CN,zh;q=0.9',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        size = 0
        with closing(requests.get(image_url, headers=request_headers, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                sys.stdout.write(filename + ' downloading...\n')
                sys.stdout.write('File Size: %0.2f MB\n' % (content_size / chunk_size / 1024))

                with open(image_path, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()
                        sys.stdout.write('In Progress: %.2f%%' % float(size / content_size * 100) + '\r')
                        sys.stdout.flush()


if __name__ == '__main__':
    spider = ImageSpider()
    # a_url = spider.get_images_links()

    # image = requests.get(
    #     'https://pi.tedcdn.com/r/talkstar-photos.s3.amazonaws.com/uploads/932e3725-d81d-4957-81ff-2fb7ca1b8389/dismalswamptextless.jpg?quality=89&w=320')
    # spider.write_file('a.jpg', image)
    spider.get_images_links()
    # spider.start_download()
