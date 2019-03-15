from concurrent.futures import ThreadPoolExecutor
import requests
import logging
from queue import Queue
import threading
from bs4 import BeautifulSoup
import time

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

class BlogNewsSpider:
    FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    # 'https://news.cnblogs.com/n/page/10/'
    BASE_URL = 'https://news.cnblogs.com'
    NEW_PAGE = '/n/page/'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0 Chrome/55.0.2883.75 Safari/537.36",
    }

    def __init__(self):
        # 使用队列存储
        self.urls = Queue()      # url队列
        self.htmls = Queue()     # 响应数据队列
        self.outputs = Queue()   # 结果输出队列

        self.event = threading.Event()
        self.executor = ThreadPoolExecutor(10)

    # 创建博客园的新闻urls，每页30条新闻
    def create_urls(self, start, end, step=1):
        for i in range(start, end+1, step):
            self.urls.put('{}{}{}/'.format(self.BASE_URL, self.NEW_PAGE, i))
        print('url创建完毕')

    # 爬取页面线程函数
    def crawler(self):
        while not self.event.is_set():
            try:
                url = self.urls.get(True, 1)
                with requests.get(url, headers=self.headers) as response:
                    html = response.text
                    self.htmls.put(html)
            except Exception as e:
                logging.info(e)
                break

    # 解析线程函数
    def parser(self):
        while not self.event.is_set():
            try:
                html = self.htmls.get(True, 1)
                soup = BeautifulSoup(html, 'lxml')
                titles = soup.select('h2.news_entry a')
                for title in titles:
                    val = title.text, self.BASE_URL+title.get('href')
                    self.outputs.put(val)
            except Exception as e:
                logging.info(e)
                break

    # 持久化数据函数
    def save(self, path):
        with open(path, 'a') as f:
            while not self.event.is_set():
                try:
                    text, url = self.outputs.get(True, 1)
                    f.write('{} {}\n'.format(text, url))
                    f.flush()
                except Exception as e:
                    logging.info(e)
                    break

    def run(self):
        # 线程池
        self.executor.submit(self.create_urls, 1, 10)
        self.executor.submit(self.parser)
        self.executor.submit(self.save, 'f:/news.txt')
        for i in range(7):
            self.executor.submit(self.crawler)

        while True:
            self.inp = input('>>>')
            if self.inp.strip() == 'q':
                self.event.set()
                print('closing ......')
                time.sleep(4)
                break


if __name__ == '__main__':
    BlogNewsSpider().run()